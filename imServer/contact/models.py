from django.db import models

# Create your models here.

class Contact(models.Model):
    Username = models.CharField(max_length = 20)
    Friend = models.CharField(max_length = 20)

    def __str__(self):
        return '%s : %s'%(self.Username, self.Friend)