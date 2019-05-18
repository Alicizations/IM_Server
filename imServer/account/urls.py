from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('info', views.info, name='info'),
    path('info/avatar', views.uploadAvatar, name='uploadAvatar'),
    path('info/<str:t_attr>', views.changeInfo, name='changeInfo'),
    path('info/user/<str:t_username>', views.othersInfo, name='othersInfo'),
    path('password', views.changePassword, name='cPassword'),
]