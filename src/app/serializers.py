# -*- encoding: utf-8 -*-
from datetime import date
from rest_framework.reverse import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Job, Build

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'name', 'description',
                  'svn_url', 'svn_username', 'svn_password',
                  'recipient', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk}, request=request)
        }


class BuildSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Build
        fields = ('id', 'number', 'created', 'job', 'updated', 'result', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
            'job': None,
        }
        # 注意: 这里用的是sprint_id, assigned用的是 obj.assigned.
        if obj.job:
            links['job'] = reverse('job-detail', kwargs={'pk': obj.job_id}, request=request)

        return links

    def validate(self, attrs):
        return attrs
