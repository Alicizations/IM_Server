from django.urls import path

from . import views

urlpatterns = [
    path('<int:seq>', views.messageTable, name='messageTable'),
]