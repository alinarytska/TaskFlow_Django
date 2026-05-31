import os
from datetime import timedelta
import django
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from test_app.models import Task, SubTask


task = Task.objects.create(
    title='Prepare presentation',
    description='Prepare materials and slides for the presentation.',
    status='new',
    deadline=timezone.now() + timedelta(days=3),
)

SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation.",
    task=task,
    status="new",
    deadline=timezone.now() + timedelta(days=2),
)

SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides.",
    task=task,
    status="new",
    deadline=timezone.now() + timedelta(days=1),
)


new_tasks = Task.objects.filter(status="new")

print("Tasks with status New:")
for task in new_tasks:
    print(task)

expired_done_subtasks = SubTask.objects.filter(status="done", deadline__lt=timezone.now(),)

print("\nDone subtasks with expired deadline:")
for subtask in expired_done_subtasks:
    print(subtask)


task_upd = Task.objects.get(title="Prepare presentation")
task_upd.status = "in_progress"
task_upd.save()

subtask_upd_1 = SubTask.objects.get(title="Gather information")
subtask_upd_1.deadline = timezone.now() - timedelta(days=2)
subtask_upd_1.save()

subtask_upd_2 = SubTask.objects.get(title="Create slides")
subtask_upd_2.description = "Create and format presentation slides."
subtask_upd_2.save()


task_del = Task.objects.get(title="Prepare presentation")
task_del.delete()
