# -*- encoding: utf-8 -*-

import json

from datetime import date
from rest_framework.reverse import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Job, Build

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    violation_info = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'name', 'description',
                  'svn_url', 'svn_username', 'svn_password',
                  'recipient', 'links', 'violation_info')

    def get_violation_info(self, obj):
        last_build = obj.builds.last()
        if last_build:
            return json.loads(last_build.result).get('violation_info')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk}, request=request)
        }


class BuildSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Build
        fields = ('id', 'number', 'created', 'job', 'result', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('build-detail', kwargs={'pk': obj.pk}, request=request),
            'job': None,
        }
        # 注意: 这里用的是sprint_id, assigned用的是 obj.assigned.
        if obj.job:
            links['job'] = reverse(
                'job-detail', kwargs={'pk': obj.job_id}, request=request)

        return links

    def validate(self, attrs):
        return attrs
