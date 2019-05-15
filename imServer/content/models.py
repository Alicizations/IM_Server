from django.db import models

# Create your models here.

class Content_Text(models.Model):
    Cid = models.AutoField(primary_key = True)
    Cstr = models.CharField(max_length = 500)
    Timestamp = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.Cid)

class Content_Image(models.Model):
    Cid = models.AutoField(primary_key = True)
    # 这里的upload_to是指定图片存储的文件夹名称，上传文件之后会自动创建
    Cimage = models.ImageField(upload_to='img')
    Timestamp = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.Cid)

class Content_AddMsg(models.Model):
    Cid = models.AutoField(primary_key = True)
    # 添加好友的请求的来源和目标用户
    From = models.CharField(max_length = 20)
    To = models.CharField(max_length = 20)
    Timestamp = models.CharField(max_length = 20)

    def __str__(self):
        return self.From + ' -> ' + self.To