from django.urls import path

from .views import create, guild_list, delete, users, info, join, leave, kick, operate, edit, applications, validate


urlpatterns = [
    path('create', create),
    path('list', guild_list),
    path('delete', delete),
    path('users', users),
    path('info', info),
    path('join', join),
    path('leave', leave),
    path('kick', kick),
    path('operate', operate),
    path('edit', edit),
    path('applications', applications),
    path('validate', validate)
]