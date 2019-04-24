from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('info/', views.info, name='info'),
    path('password/', views.changePassword, name='cPassword'),
]