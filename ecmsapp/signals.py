from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if user_status == 'customer':
#             group = Group.objects.get(name='customer')
#             user.groups.add(group)
#             Customer.objects.create(
#                 user=instance,
#                 name=instance.username,)
