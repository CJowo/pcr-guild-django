"""pcr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.views import static
from pcr import settings

def index(request, *args, **kwargs):
    return render(request, 'index.html')
    
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/guild/', include('guild.urls')),
    path('api/battle/', include('battle.urls')),
    path('api/character/', include('character.urls')),
    path('api/admin/', include('admin.urls')),
    path('api/report/', include('report.urls')),
    re_path('^(?!(js|css|img|fonts|statics)).*', index),
    re_path('(?P<path>^(js|css|img|fonts|statics).*)', static.serve, { 'document_root': settings.STATIC_ROOT })
]
