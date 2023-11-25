from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import Signal 
from django.db.models.signals import m2m_changed
from .models import Task

task_created = Signal()
task_updated = Signal()
task_completed = Signal()
task_deleted = Signal()

@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, **kwarfs):
    task_created.send(sender=instance)

@receiver(post_save, sender=Task)
def task_updated_handler(sender, instance, **kwarfs):
    task_updated.send(sender=instance)

@receiver(post_save, sender=Task)
def task_completed_handler(sender, instance, **kwarfs):
    task_completed.send(sender=instance)

@receiver(post_save, sender=Task)
def task_deleted_handler(sender, instance, **kwarfs):
    task_deleted.send(sender=instance)







    



