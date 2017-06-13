from django.core.management.base import BaseCommand, CommandError
from app.models import Task

class Command(BaseCommand):
    help = 'Closes the specified Task'

    def add_arguments(self, parser):
        parser.add_argument('task_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for task_id in options['task_id']:
            try:
                task = Task.objects.get(pk=task_id)
            except Task.DoesNotExist:
                raise CommandError('Task "%s" does not exist' % task_id)

            task.status = Task.STATUS_DONE
            task.save()

            self.stdout.write('Successfully closed task "%s"' % task_id)