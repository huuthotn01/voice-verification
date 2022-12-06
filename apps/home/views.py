# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo, UserVoice
from urllib.parse import urlparse, parse_qs
import json
import os
from datetime import datetime

VOICE_FAIL_PATH = "voice_file/"

# Enroll

def index(request):
    context = {'segment': 'enroll', 'enrollUsername': True, 'msg': ''}

    html_template = loader.get_template('home/enroll.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def enrollCheckUsername(request):
    name = request.POST['enroll-name']
    username = request.POST['enroll-username']
    email = request.POST['enroll-email']
    password = request.POST['enroll-password']
    dob = request.POST['enroll-dob']

    # check username
    checkUsername = UserInfo.objects.filter(username=username)
    if checkUsername.count() > 0:
        context = {'segment': 'enroll', 'enrollUsername': True, 'msg': 'Username existed'}
    else:
        context = {'segment': 'enroll', 'enrollVoice': True, 'name': name, 'username': username, 'email': email, 'password': password, 'dob': dob}

    html_template = loader.get_template('home/enroll.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def enrollCheckVoice(request):
    username = request.GET.get('username')
    counter = request.GET.get('counter')
    counter = int(counter)
    reqData = request.body
    counter += 1
    if not os.path.exists(VOICE_FAIL_PATH + username): os.mkdir(VOICE_FAIL_PATH + username)
    filename = VOICE_FAIL_PATH + username + "/" + username + "_" + str(counter) +  ".wav"
    with open(filename, 'ab') as f:
        f.write(reqData)

    # check whether voice valid
    return HttpResponse(json.dumps({"ok":True}))

@csrf_exempt
def enrollDone(request):
    # save to db
    name = request.POST['name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    dob = request.POST['dob']
    dob = datetime.strptime(dob, '%Y-%m-%d')
    userInfo = UserInfo(username=username, name=name, email=email, password=password, dob=dob)
    userInfo.save()
    for i in range(5):
        filePath = username + "/" + username + "_" + str(i + 1)
        userVoice = UserVoice(username=username, enroll_voice=filePath)
        userVoice.save()

    context = {'segment': 'enroll', 'enrollDone': True, 'username': username}
    html_template = loader.get_template('home/enroll.html')
    return HttpResponse(html_template.render(context, request))


# Sign in

def signin(request):
    context = {'segment': 'signin', 'signinUsername': True, 'msg': ''}

    html_template = loader.get_template('home/sign-in.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def signinCheckUsername(request):
    username = request.POST['signin-username']

    # check username
    checkUsername = UserInfo.objects.filter(username=username)
    if checkUsername.count() == 0:
        context = {'segment': 'signin', 'signinUsername': True, 'msg': 'Username not existed'}
    else:
        context = {'segment': 'signin', 'signinVoice': True, 'username': username}

    html_template = loader.get_template('home/sign-in.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def signinCheckVoice(request):
    username = request.GET.get('username')
    reqData = request.body
    # send voice to AI to check
    return HttpResponse(json.dumps({"ok":True}))

@csrf_exempt
def signinCheckPassword(request):
    username = request.POST['username']
    if 'pwd-password' not in request.POST:
        context = {'segment': 'signin', 'signinPassword': True, 'msg': '', 'username': username}
    else:
        password = request.POST['pwd-password']
        checkAccount = UserInfo.objects.filter(username=username, password=password)
        if checkAccount.count() == 0:
            context = {'segment': 'signin', 'signinPassword': True, 'msg': 'Wrong password', 'username': username}
        else:
            context = {'segment': 'signin', 'signinDone': True, 'msg': '', 'username': username}

    html_template = loader.get_template('home/sign-in.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def signinDone(request):
    username = request.POST['username']
    context = {'segment': 'signin', 'signinDone': True, 'username': username, 'is_authenticated': True}
    html_template = loader.get_template('home/sign-in.html')
    return HttpResponse(html_template.render(context, request))


# Other routes

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
