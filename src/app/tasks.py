# -*- encoding: utf-8 -*-

from .models import Job, Build
from django.conf import settings
from lintjenkins import LintJenkins
import json


def update_build_info():
    return 'xxxxxxxxx'
    lint_jenkins = LintJenkins(settings.JENKINS_URL,
                               username=settings.JENKINS_USER,
                               password=settings.JENKINS_TOKEN)
    for job in Job.objects.all():
        remote_build_numbers = lint_jenkins.get_build_numbers(job.name)
        local_build_numbers = [int(build['number']) for build in job.builds.values('number')]
        new_build_numbers = list(set(remote_build_numbers) - set(local_build_numbers))
        for new_build_number in new_build_numbers:
            build_info = lint_jenkins.get_build_info(job.name, new_build_number)
            job.builds.create(
                number=new_build_number,
                result=json.dumps(build_info))
