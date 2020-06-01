from django.urls import path

from .views import *


urlpatterns = [
    path('create', create),
    path('close', close),
    path('info', info)
]