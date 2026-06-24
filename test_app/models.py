from django.db import models
from django.utils import timezone
from .managers import SoftDeleteManager


status_choices = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]


class Task(models.Model):
    title = models.CharField(
        max_length=100,
        # unique_for_date='created_at'
    )
    description = models.TextField()
    categories = models.ManyToManyField('Category')
    status = models.CharField(max_length=50, choices=status_choices)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_task'

        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_task_title'
            )
        ]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=50, choices=status_choices)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_subtask'

        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_subtask_title',
            )
        ]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'task_manager_category'

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_category_name',
            )
        ]

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name
