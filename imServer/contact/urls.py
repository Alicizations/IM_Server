from django.urls import path

from . import views

urlpatterns = [
    path('info', views.info, name='info'),
    path('add', views.add, name='add'),
    path('delete', views.delete, name='delete'),
]