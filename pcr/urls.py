"""pcr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.shortcuts import render
from django.views import static

from . import settings
from login.views import login, register, logout, remove, set_password, set_staff, get_detail, get_detail_all, set_detail
from box.views import character_add, character_edit, character_remove


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/login/', login),
    path('api/register/', register),
    path('api/logout/', logout),
    path('api/remove/', remove),
    path('api/set_password/', set_password),
    path('api/set_staff/', set_staff),
    path('api/set_detail/', set_detail),
    path('api/get_detail/', get_detail),
    path('api/get_detail_all/', get_detail_all),
    path('api/character_add/', character_add),
    path('api/character_edit/', character_edit),
    path('api/character_remove/', character_remove),
    re_path('^(?!static).*', lambda request: render(request, 'index.html'))
]

if not settings.DEBUG:
    urlpatterns += [
        re_path('^static/(?P<path>.*)', static.serve, { 'document_root': settings.STATIC_ROOT })
    ]