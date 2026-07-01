from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Task


@receiver(pre_save, sender=Task)
def save_previous_status(sender, instance, **kwargs):
    """
    Сохраняет предыдущий статус задачи перед обновлением.
    """
    if instance.pk:
        try:
            previous_task = Task.objects.get(pk=instance.pk)
            instance._previous_status = previous_task.status
        except Task.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Task)
def send_status_notification(sender, instance, created, **kwargs):
    """
    Отправляет уведомление владельцу задачи,
    если статус изменился.
    """
    if created:
        return

    if instance._previous_status == instance.status:
        return

    if not instance.owner or not instance.owner.email:
        return

    if instance.status == 'done':
        subject = 'Task closed'
        message = (
            f'Hello {instance.owner.username},\n\n'
            f'Your task "{instance.title}" has been closed.'
        )
    else:
        subject = 'Task status updated'
        message = (
            f'Hello {instance.owner.username},\n\n'
            f'The status of your task "{instance.title}" '
            f'has been changed from '
            f'"{instance._previous_status}" to "{instance.get_status_display()}".'
        )

    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@example.com',
        recipient_list=[instance.owner.email],
        fail_silently=False,
    )
