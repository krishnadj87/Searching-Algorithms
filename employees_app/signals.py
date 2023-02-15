from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile,Employee
from django.dispatch import receiver
from django.conf import settings
from django.core.cache import cache


# creating user defualt user profile 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = Profile(user=instance, address='Jalandhar,Punjab')
        user_profile.save() # saving profile obj  
        cache.clear()       # clearing all caches 
   