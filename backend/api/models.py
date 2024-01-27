from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission  # Add these imports
from django.db.models.signals import post_save
# Create your models here.



class User(AbstractUser):
    # groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    # user_permissions = models.ManyToManyField(
    # Permission, related_name='custom_user_permissions'
    # )
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=300)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.full_name
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
