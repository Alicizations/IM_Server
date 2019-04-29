from django.contrib import admin
from .models import Content_Text
from .models import Content_Image

# Register your models here.

admin.site.register(Content_Text)
admin.site.register(Content_Image)
