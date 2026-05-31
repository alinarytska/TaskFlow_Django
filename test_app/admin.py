from django.contrib import admin
from test_app.models import Task, SubTask, Category


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = [
        'short_title',
        'description',
        'status',
        'deadline',
        'created_at',
    ]

    search_fields = [
        'title',
        'description',
    ]

    ordering = [
        'deadline',
    ]

    list_filter = [
        'status',
    ]

    list_editable = [
        'status',
        'deadline',
    ]

    inlines = [
        SubTaskInline,
    ]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title

    short_title.short_description = "Title"


@admin.register(SubTask)
class SubTaskModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'task',
        'status',
        'deadline',
        'created_at',
    ]

    search_fields = [
        'title',
        'description',
    ]

    ordering = [
        'deadline',
    ]

    list_filter = [
        'status',
    ]

    list_editable = [
        'status',
        'deadline',
    ]

    actions = [
        'set_status_done',
    ]

    def set_status_done(self, request, queryset):
        queryset.update(status='done')

    set_status_done.short_description = "Set selected subtasks to Done"


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']

    search_fields = ['name']
