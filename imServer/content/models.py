from django.db import models

# Create your models here.

class Content_Text(models.Model):
    Cid = models.AutoField(primary_key = True)
    Cstr = models.CharField(max_length = 500)

    def __str__(self):
        return self.Cid

class Content_Image(models.Model):
    Cid = models.AutoField(primary_key = True)
    Cimage = models.IntegerField(default = -1)

    def __str__(self):
        return self.Cid