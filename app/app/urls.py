"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test_1, name='tset'),
    path('', views.homeview, name='homeview'),
    path('validation/', views.validation, name='validation'),
    path('insert/', views.insert_view),
    path('lookup/', views.lookup_view),
    path('some_view/',views.some_view),
    path('check_data/',views.check_data),
    path('check_data_val/',views.check_data_val),
    path('about/',views.team),
    path(r'robots.txt', views.honeypot)
]
