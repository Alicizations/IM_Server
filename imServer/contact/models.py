from django.db import models

# Create your models here.

class Contact(models.Model):
    UserName = models.AutoField(primary_key = True)
    Friends = models.CharField(max_length = 200)

    def __str__(self):
        return self.Friends