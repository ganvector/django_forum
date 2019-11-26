from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from.models import Perfil


@receiver(post_save, sender=User)
def cria_perfil(sender, instance, created, *args, **kwargs):
    if(created):
        p = Perfil(user=instance)
        p.save()


@receiver(post_save, sender=User)
def salva_perfil(sender, instance, *args, **kwargs):
    instance.perfil.save()