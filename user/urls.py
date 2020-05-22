from django.urls import path

from .views import register, login, logout, edit, refresh_token


urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('edit', edit),
    path('refresh_token', refresh_token),
]