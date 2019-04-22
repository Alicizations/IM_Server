# from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from .models import User

# Create your views here.

def register(request):

    if request.method != 'POST':
        return HttpResponse("register page")

    response = {'state':'ok', 'msg':'register successfully'}

    # 获取参数
    try:
        t_username = request.POST['username']
        t_password = request.POST['password']
    except Exception as e:
        response = {'state':'fail', 'msg':'POST parameter error'}
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        response = {'state':'fail', 'msg':'db error'}
    else:
        if t_user.count() == 0:
            User.objects.create(
                Username = t_username,
                Password = t_password
            )
        else:
            response = {'state':'failed', 'msg':'repeat username'}

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def login(request):
    if request.method != 'POST':
        return HttpResponse("login page")

    response = {'state':'ok', 'msg':'login successfully'}

    # 获取参数
    try:
        t_username = request.POST['username']
        t_password = request.POST['password']
    except Exception as e:
        response = {'state':'fail', 'msg':'POST parameter error'}
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        response = {'state':'fail', 'msg':'db error'}
    else:
        if t_user.count() <= 0:
            response = {'state':'failed', 'msg':'username or password error'}

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def info(request, t_username):
    if request.method == 'POST':
        return HttpResponse("fail")

    response = {'state':'fail', 'msg':'no data'}

    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        response = {'state':'fail', 'msg':'db error'}
    else:
        if t_user.count() == 1:
            temp = model_to_dict(t_user[0])
            response = {'state':'ok', 'msg':'ok', "data":temp}

    return HttpResponse(json.dumps(response), content_type = 'application/json')
            