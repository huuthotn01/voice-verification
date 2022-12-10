# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Enroll
    path('enroll-check-username', views.enrollCheckUsername, name='enrollCheckUsername'),
    path('enroll-check-voice', views.enrollCheckVoice, name="enrollCheckVoice"),
    path('enroll-done', views.enrollDone, name="enrollDone"),

    # Sign in
    path('signin', views.signin, name="signin"),
    path('signin-check-username', views.signinCheckUsername, name="signinCheckUsername"),
    path('signin-check-voice', views.signinCheckVoice, name="signinCheckVoice"),
    path('signin-check-password', views.signinCheckPassword, name="signinCheckPassword"),
    path('signin-done', views.signinDone, name='signinDone'),

    # Logout
    path('logout', views.logout, name="logout"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
