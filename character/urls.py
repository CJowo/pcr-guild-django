from django.urls import path

from .views import *


urlpatterns = [
    path('create', create),
    path('edit', edit),
    path('delete', delete)
]