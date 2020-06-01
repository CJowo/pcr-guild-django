from django.urls import path

from .views import *


urlpatterns = [
    path('create', create),
    path('edit', edit),
    path('delete', delete),
    path('list', report_list),
    path('mylist', my_list),
    path('today', today)
]