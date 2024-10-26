from django.db.models.signals import post_save
from .models import User, Profile
from django.dispatch import receiver
from ticketandpayment.models import AdminModule

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_admin:
            AdminModule.objects.create(user=instance)
        else:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    
    if instance.is_admin:
        instance.admin_module.save()
    else:
        instance.user_profile.save()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_admin:
#             AdminModule.objects.create(user=instance)
#         else:
#             Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
    
#     if instance.is_admin:
#         instance.admin_module.save()
#     else:
#         instance.user_profile.save()

# '''if error occurs in django admin '''
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if not hasattr(instance, 'profile'):
#             Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()


