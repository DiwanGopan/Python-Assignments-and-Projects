"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .views import *

urlpatterns = [
    path('',index   ,name='home'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('changepassword/',change_password,name='change_password'),
    path('editprofile/',editprofile,name='edit_profile'),
    # member

    path('add-member/',add_member,name='add_member'),
    path('all-member/',all_member,name='all_member'),
    path('mem-profile/',mem_profile,name='mem_profile'),
    path('mem-change-password/',mem_change_password,name='mem_change_password'),
    path('mem-edit-profile/',mem_edit_profile,name='mem_edit_profile'),
    path('delete-member/<int:pk>',delete_member,name='delete_member'),
    path('mem-all-member/',mem_all_member,name='mem_all_member'),
    # notice

    path('add-notice/',add_notice,name='add_notice'),
    path('all-notice/',all_notice,name='all_notice'),
    path('mem-all-notice/',mem_all_notice,name='mem_all_notice'),
    path('delete-notice/<int:pk>',delete_notice,name='delete_notice'),
    # Event 

    path('add-event/',add_event,name='add_event'),
    path('all-event/',all_event,name='all_event'),
    path('mem-all-event/',mem_all_event,name='mem_all_event'),
    path('delete-event/<int:pk>',delete_event,name='delete_event'),
]
