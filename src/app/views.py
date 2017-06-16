#-*- encoding: utf-8 -*-

from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Sprint, Task
from .serializers import SprintSerializer, UserSerializer, TaskSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
User = get_user_model()

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


class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    search_fields = ('name',)
    ordering_fields = ('end','name')
    filter_fields  = ('name', )
    # 普通的字段匹配这样够了,如果需要实现高级匹配比如日期基于某个范围等,就需要定义自己的FilterSet类了
    # http://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ('name','description')
    ordering_fields = ('name','order','started', 'due','completed')
    filter_fields = ('assigned', )
    # 用的是pk来过滤user的.

class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD,)






class UserDefineViewSet(viewsets.ViewSet):
    """
    有时需要抽象一些资源, 并没有对应的Model,Serializer. 这时需要手动实现ViewSet一些方法以达到类似于ModelViewSet的效果 .
    """
    def list(self, request):
        # queryset = User.objects.all()
        # serializer = UserSerializer(queryset, many=True)
        return Response([])

    def retrieve(self, request, pk=None):
        # queryset = User.objects.all()
        # user = get_object_or_404(queryset, pk=pk)
        # serializer = UserSerializer(user)
        return Response({})