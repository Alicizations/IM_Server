from django.db import models

# Create your models here.

class Msg(models.Model):
    Username = models.CharField(max_length = 20)
    Seq = models.IntegerField(default = 0)
    From = models.CharField(max_length = 20)
    Type = models.CharField(max_length = 10)
    ContentID = models.IntegerField(default = 0)