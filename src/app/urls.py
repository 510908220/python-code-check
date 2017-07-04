# -*- encoding: utf-8 -*-
from . import views
from rest_framework import routers
router = routers.DefaultRouter()  # DefaultRouter会生成rootview
router.register(r'jobs', views.JobViewSet)
router.register(r'builds', views.BuildViewSet)
# router.register(r'userdefines', views.UserDefineViewSet, 'userdefine')
