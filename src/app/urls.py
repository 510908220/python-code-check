# -*- encoding: utf-8 -*-
from . import views
from rest_framework import routers
router = routers.DefaultRouter() # DefaultRouter会生成rootview
router.register(r'sprints', views.SprintViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'userdefines', views.UserDefineViewSet, 'userdefine')