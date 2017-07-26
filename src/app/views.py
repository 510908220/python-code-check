#-*- encoding: utf-8 -*-

import json
import logging

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import authentication, filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from lintjenkins import LintJenkins
from silk.profiling.profiler import silk_profile

from .models import Build, Job
from .serializers import BuildSerializer, JobSerializer

logger = logging.getLogger('django')


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1001
    # XXX: 暂时写死,后续前端再添加分页支持

# Create your views here.


class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication
    )
    permission_classes = (
        permissions.AllowAny,  # TODO: 上下后需要改为登陆用户
    )
    pagination_class = StandardResultsSetPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )


class JobViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    search_fields = ('name',)
    ordering_fields = ('name',)
    filter_fields = ('name', )
    # 普通的字段匹配这样够了,如果需要实现高级匹配比如日期基于某个范围等,就需要定义自己的FilterSet类了
    # http://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend

    def perform_create(self, serializer):
        serializer.save()
        # 创建jenkins job
        lint_jenkins = LintJenkins(settings.JENKINS_URL,
                                   username=settings.JENKINS_USER,
                                   password=settings.JENKINS_TOKEN)
        job_info = serializer.data
        logger.info(job_info)
        try:
            lint_jenkins.add_job(svn=job_info['svn_url'],
                                 username=job_info['svn_username'],
                                 password=job_info['svn_password'],
                                 job_name=job_info['name'])
        except Exception as e:
            logger.exception(e)
            Job.objects.filter(id=job_info['id']).delete()
            raise Exception(e)

        logger.info('create params:%s', serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer.data.sort(key=lambda x: x['violation_info']['violation_num'], reverse=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer.data.sort(key=lambda x: x['violation_info']['violation_num'], reverse=True)
        return Response(serializer.data)


class BuildViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    search_fields = ('job__name',)
    ordering_fields = ('created',)
    filter_fields = ('job__name', )
    # 用的是pk来过滤user的.


class StatisticViewSet(viewsets.ViewSet):
    """
    有时需要抽象一些资源, 并没有对应的Model,Serializer. 这时需要手动实现ViewSet一些方法以达到类似于ModelViewSet的效果 .
    """

    # def list(self, request):
    #     with silk_profile(name='View User'):
    #         queryset = Job.objects.all()
    #         serializer = JobSerializer(queryset, many=True, context={'request': request})
    #         import time
    #         time.sleep(2)
    #         return Response(serializer.data)

    def retrieve(self, request, pk=None):
        job = get_object_or_404(Job, pk=pk)

        # STEP1:按照jenkins 构建号排序(从大到小)、填充数据
        rows = []
        charts = {
            'labels': [],
            'violation_nums': [],
            'violation_file_nums': []
        }
        builds = job.builds.order_by('-number')[:50]
        for build in builds:
            lint_result = json.loads(build.result)
            violation_num = lint_result['violation_info']['violation_num']
            violation_file_num = lint_result['violation_info']['violation_file_num']
            rows.append({
                'number': build.number,
                'violation_num': violation_num,
                'violation_num_add': 0,
                'violation_file_num': violation_file_num,
                'violation_file_num_add': 0,
                'created': lint_result['datetime']
            })
            charts['labels'].append(build.number)
            charts['violation_nums'].append(violation_num)
            charts['violation_file_nums'].append(violation_file_num)

        # STEP2:填充多次构建之间的差异值,即violation_num_add和violation_file_num_add
        for index, row in enumerate(rows):
            try:
                row['violation_num_add'] = row['violation_num'] - rows[index + 1]['violation_num']
                row['violation_file_num_add'] = row['violation_file_num'] - rows[index + 1]['violation_file_num']
            except:
                pass

        # STEP3:返回统计数据

        data = {
            'created': '',
            'violation_num': 0,
            'violation_num_add': 0,
            'violation_file_num': 0,
            'violation_file_num_add': 0,
        }
        if rows:
            for k in data:
                data[k] = rows[0].get(k)
        data['rows'] = rows
        data['job_name'] = job.name

        data['report_url'] = settings.JENKINS_URL + '/job/{job_name}/violations/'.format(job_name=job.name)

        # 图表按构建号升序显示
        for k in charts:
            charts[k].reverse()
        data['charts'] = charts
        return Response(data)
