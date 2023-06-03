from django.db import models

# Create your models here.

from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  
from django.utils.translation import gettext_lazy as _  
 
# Create your models here.

class User(AbstractUser):
    
    mobile=models.CharField(_("Mobile") ,max_length=15)
    def __str__(self) :
        return self.username
