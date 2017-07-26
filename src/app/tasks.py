# -*- encoding: utf-8 -*-

import json
import logging
import time

from django.conf import settings
from django_q.tasks import Async
from djmail.template_mail import InlineCSSTemplateMail

from lintjenkins import LintJenkins

from .models import Build, Job

logger = logging.getLogger('jenkins')


def update_build_info():
    lint_jenkins = LintJenkins(settings.JENKINS_URL,
                               username=settings.JENKINS_USER,
                               password=settings.JENKINS_TOKEN)
    for job in Job.objects.all():
        remote_build_numbers = lint_jenkins.get_build_numbers(job.name)
        local_build_numbers = [int(build['number']) for build in job.builds.values('number')]
        new_build_numbers = list(set(remote_build_numbers) - set(local_build_numbers))
        new_build_numbers.sort()

        to = job.recipient.split(";")
        for new_build_number in new_build_numbers:
            try:
                build_info = lint_jenkins.get_build_info(job.name, new_build_number)
            except Exception as e:
                logger.exception(e)
                continue

            job.builds.create(
                number=new_build_number,
                result=json.dumps(build_info))
            if build_info['violation_info']['violation_num'] > job.violation_threshold_num:
                build_info.update({
                    'build_number': new_build_number,
                    'report_url': settings.JENKINS_URL + '/job/{job_name}/{build_number}/violations/'.format(
                        job_name=job.name,
                        build_number=new_build_number
                    )
                })
                opts = {
                    'task_name': 'send_email',
                    'group': 'violation'
                }
                ctx = {
                    'title': new_build_number,
                    'content':  build_info
                }
                Async('app.tasks.send_email', to, ctx, q_options=opts).run()
                time.sleep(0.1)
        time.sleep(1)


def send_email(to, ctx):
    o = InlineCSSTemplateMail("alert")
    if isinstance(to, str):
        to = [to]
    o.send(to, ctx)
