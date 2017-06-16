# -*- encoding: utf-8 -*-
from datetime import date
from rest_framework.reverse import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Sprint, Task

User = get_user_model()


class SprintSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'links')
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail', kwargs={'pk':obj.pk}, request=request)
        }
    def validate_end(self, value):
        new = self.instance is None
        changed = self.instance and self.instance.end != value
        if (new or changed) and (value < date.today()):
            msg = "End date cannot be in the past"
            raise serializers.ValidationError(msg)
        return value

class TaskSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD,
        required=False,
        allow_null=True,
        queryset=User.objects.all()
    )
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'order',
                  'assigned', 'started', 'due', 'completed', 'status_display', 'links')

        # https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_FOO_display
        # 对于有 choices 的字段,会有一个 get_FOO_display()方法
    def get_status_display(self, obj):
        return obj.get_status_display()
    def get_links(self, obj):
        request = self.context['request']
        links =  {
            'self': reverse('task-detail', kwargs={'pk':obj.pk}, request=request),
            'sprint':None,
            'assigned':None
        }
        # 注意: 这里用的是sprint_id, assigned用的是 obj.assigned.
        if obj.sprint:
            links['sprint'] =  reverse('sprint-detail', kwargs={'pk':obj.sprint_id}, request=request)
        if obj.assigned:
            links['assigned'] = reverse('user-detail', kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)
        return links
    
    def validate(self, attrs):
        return attrs

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: obj.get_username()}, request=request)
        }