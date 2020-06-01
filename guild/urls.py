from django.urls import path

from .views import *


urlpatterns = [
    path('create', create),
    path('list', guild_list),
    path('delete', delete),
    path('users', users),
    path('boxes', boxes),
    path('info', info),
    path('join', join),
    path('leave', leave),
    path('kick', kick),
    path('operate', operate),
    path('edit', edit),
    path('applications', applications),
    path('validate', validate)
]