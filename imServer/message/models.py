from django.db import models
from account.models import *

# Create your models here.

class Msg(models.Model):
    Username = models.CharField(max_length = 20)
    Seq = models.IntegerField(default = 0)
    From = models.CharField(max_length = 20)
    Type = models.CharField(max_length = 10)
    ContentID = models.IntegerField(default = 0)

    def __str__(self):
        return self.Username

class UserSeq(models.Model):
    User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'seq')
    Seq = models.IntegerField(default = 0)

    def __str___(self):
        return '%s: %d' % (self.User.Username, self.Seq)