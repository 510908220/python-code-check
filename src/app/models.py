from __future__ import unicode_literals
from django.conf import settings

from django.db import models

# Create your models here.

#  https://www.processon.com/apps/59197d37e4b0bcc15ca2e55c
#


class Job(models.Model):

    class Meta:
        db_table = 'jobs'

    name = models.CharField(unique=True, max_length=250)
    description = models.TextField(blank=True, default='')
    svn_url = models.TextField()
    svn_username = models.TextField(blank=True, default='')
    svn_password = models.TextField(blank=True, default='')

    recipient = models.TextField()
    violation_threshold_num = models.IntegerField(default=888)

    def __str__(self):
        return self.name


class Build(models.Model):

    class Meta:
        db_table = 'builds'

    number = models.IntegerField()
    job = models.ForeignKey(Job, related_name="builds")
    created = models.DateTimeField(auto_now_add=True)
    result = models.TextField(default="")

    def __str__(self):
        return "{0}:{1}".format(self.job.name, self.number)
