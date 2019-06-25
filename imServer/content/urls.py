from django.urls import path

from . import views

urlpatterns = [
    path('text', views.text, name='text'),
    path('image', views.image, name='image'),
    path('add', views.add, name='add'),
    path('text/<int:text_id>', views.text_detail, name='text_detail'),
    path('image/<int:image_id>', views.image_detail, name='image_detail'),
    path('delete/<str:t_user>', views.deleteContact, name='deleteContact'),
]