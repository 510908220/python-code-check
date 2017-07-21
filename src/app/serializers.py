# -*- encoding: utf-8 -*-

import json
from datetime import date, datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Build, Job

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    violation_info = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'name', 'description',
                  'svn_url', 'svn_username', 'svn_password',
                  'recipient', 'violation_threshold_num', 'links', 'violation_info')

    def get_violation_info(self, obj):
        last_build = obj.builds.last()
        violation_info = {
            "violation_file_num": -1,
            'violation_num': -1,
            'created': datetime.now(),
            'health_url': '/static/img/rain.png'
        }
        if not last_build:
            return violation_info

        violation_info = json.loads(last_build.result).get('violation_info')
        if violation_info['violation_num'] >= obj.violation_threshold_num:
            health_url = '/static/img/rain.png'
        else:
            health_url = '/static/img/sun.png'

        violation_info.update({
            'created': last_build.created,
            'health_url': health_url
        })

        return violation_info

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
