#-*- encoding: utf-8 -*-

import json


from django.shortcuts import get_object_or_404

from silk.profiling.profiler import silk_profile

from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Job, Build
from .serializers import JobSerializer, BuildSerializer

from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


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
        builds = job.builds.order_by('-number')
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
                'created': build.created
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
            'job_name': job.name,
            'violation_num': 0,
            'violation_num_add': 0,
            'violation_file_num': 0,
            'violation_file_num_add': 0,
        }
        if rows:
            for k in data:
                data[k] = rows[0].get(k)
        data['rows'] = rows

        # 图表按构建号升序显示
        for k in charts:
            charts[k].reverse()
        data['charts'] = charts
        return Response(data)
