from django.urls import path

from .views import register, login, info, logout, edit, refresh_token


urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('info', info),
    path('edit', edit),
    path('refresh_token', refresh_token),
]