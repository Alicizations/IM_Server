from django.db import models
from system.storage import ImageStorage

# Create your models here.

class User(models.Model):
    UserID = models.AutoField(primary_key = True)
    Username = models.CharField(max_length = 20)
    Password = models.CharField(max_length = 20)
    Gender = models.CharField(max_length = 10)
    Region = models.CharField(max_length = 20)
    Nickname = models.CharField(max_length = 20)
    # Avatar = models.CharField(max_length = 100)
    Avatar = models.ImageField(upload_to = 'avatar', storage = ImageStorage(), default = 'avatar/default.jpg') 
    Description = models.CharField(max_length = 40)

    def __str__(self):
        return self.Username
