from django.contrib import admin
from test_app.models import Task, SubTask, Category


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'status',
        'deadline',
        'created_at'
    ]

    search_fields = [
        'title',
        'description'
    ]

    ordering = [
        'deadline'
    ]

    list_filter = [
        'status',
    ]

    list_editable = [
        'status',
        'deadline'
    ]


@admin.register(SubTask)
class SubTaskModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'task',
        'status',
        'deadline',
        'created_at'
    ]

    search_fields = [
        'title',
        'description'
    ]

    ordering = [
        'deadline'
    ]

    list_filter = [
        'status',
    ]

    list_editable = [
        'status',
        'deadline'
    ]


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']

    search_fields = ['name']


