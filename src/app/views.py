#-*- encoding: utf-8 -*-
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
        permissions.IsAuthenticated,
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


# class UserDefineViewSet(viewsets.ViewSet):
#     """
#     有时需要抽象一些资源, 并没有对应的Model,Serializer. 这时需要手动实现ViewSet一些方法以达到类似于ModelViewSet的效果 .
#     """

#     def list(self, request):
#         with silk_profile(name='View User'):
#             queryset = User.objects.all()
#             serializer = UserSerializer(queryset, many=True, context={'request': request})
#             import time
#             time.sleep(2)
#             return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         # queryset = User.objects.all()
#         # user = get_object_or_404(queryset, pk=pk)
#         # serializer = UserSerializer(user)
#         return Response({})
