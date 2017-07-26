# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django_q.models import Schedule
from django_q.tasks import schedule


class Command(BaseCommand):
    help = 'create schedule'

    def handle(self, *args, **options):
        schedule('app.tasks.update_build_info',
                 name='update_build_info',
                 schedule_type=Schedule.MINUTES,
                 minutes=10,
                 q_options={
                     'task_name': 'update_build_info'}
                 )
