from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import Signal 
from django.db.models.signals import m2m_changed

task_created = Signal()
task_updated = Signal()
task_completed = Signal()

@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, **kwarfs):
    task_created.send(sender=instance)

@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, **kwarfs):
    task_updated.send(sender=instance)

@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, **kwarfs):
    task_completed.send(sender=instance)

    



