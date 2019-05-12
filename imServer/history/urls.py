from django.urls import path

from . import views

urlpatterns = [
    path('personal', views.personal, name='personal'),
    # 群聊消息记录，暂未实现
    path('group', views.group, name='group'),
]