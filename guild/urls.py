from django.urls import path

from .views import create, guild_list, delete, users, join, kick, operate, applications, validate


urlpatterns = [
    path('create', create),
    path('list', guild_list),
    path('delete', delete),
    path('users', users),
    path('join', join),
    path('kick', kick),
    path('operate', operate),
    path('applications', applications),
    path('validate', validate)
]