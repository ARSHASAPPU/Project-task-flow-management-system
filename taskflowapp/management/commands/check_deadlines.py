from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from taskflowapp.models import Task, Notification

class Command(BaseCommand):
    help = 'Checks for tasks with deadlines approaching and creates notifications'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        upcoming_tasks = Task.objects.filter(
            deadline__lte=tomorrow,
            status__in=["To Do", "In Progress"]
        )

        added_count = 0

        for task in upcoming_tasks:
            if not Notification.objects.filter(
                user=task.assigned_to,
                message__icontains=task.title,
                type='deadline'
            ).exists():
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f'Deadline approaching for task "{task.title}".',
                    type='deadline'
                )
                added_count += 1

        self.stdout.write(self.style.SUCCESS(f'✔ Deadline notifications checked. Added {added_count} new.'))
