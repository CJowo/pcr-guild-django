from django.urls import path

from .views import *


urlpatterns = [
    path('validate', validate),
    path('info', info),
    path('password', password),
    path('edit', edit)
]