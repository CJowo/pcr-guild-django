from django.urls import path

from .views import *


urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('info', info),
    path('edit', edit),
    path('refresh_token', refresh_token),
]