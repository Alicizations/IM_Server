# from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from .models import User

# Create your views here.

def register(request):
    response = {'state':'fail', 'msg':'no msg'}

    if 'login_id' in request.session:
        response['msg'] = 'already login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    if request.method != 'POST':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 获取参数
    try:
        t_username = request.POST['username']
        t_password = request.POST['password']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        response['msg'] = 'db error'
    else:
        if t_user.count() == 0:
            User.objects.create(
                Username = t_username,
                Password = t_password
            )
            response['state'] = 'ok'
            response['msg'] = 'register successfully'
        else:
            response['msg'] = 'repeat username'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def logout(request):
    response = {'state':'fail', 'msg':'no msg'}
    # 只允许通过GET方法退出登录
    if request.method != 'GET':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    try:
        del request.session['login_id']
    except KeyError:
        response['msg'] = 'no login'
    else:
        response['state'] = 'ok'
        response['msg'] = 'logout successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def login(request):
    response = {'state':'fail', 'msg':'no msg'}

    if request.method != 'POST':
        if 'login_id' in request.session:
            response['state'] = 'ok'
            response['msg'] = 'already login'
        else:
            response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 获取参数
    try:
        t_username = request.POST['username']
        t_password = request.POST['password']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username, Password = t_password)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_user.count() <= 0:
            response['msg'] = 'username or password error'
        else:
            response['state'] = 'ok'
            response['msg'] = 'login successfully'
            request.session['login_id'] = t_username

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def info(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    if request.method == 'POST':
        # 获取参数
        try:
            t_phone = request.POST['phone']
            t_email = request.POST['email']
            t_nickname = request.POST['nickname']
            t_avator = request.POST['avator']
            t_description = request.POST['description']
        except Exception as e:
            response['msg'] = 'POST parameter error'
            return HttpResponse(json.dumps(response), content_type = 'application/json')

        # 数据库操作
        try:
            t_user = User.objects.filter(Username = t_username)
        except Exception as e:
            response['msg'] = 'db error'
            return HttpResponse(json.dumps(response), content_type = 'application/json')
        else:
            if t_user.count() == 1:
                temp = model_to_dict(t_user[0])
                response = {'state':'ok', 'msg':'ok', "data":temp}
            else:
                response['msg'] = 'no data'

        return HttpResponse(json.dumps(response), content_type = 'application/json')

    if request.method != 'GET':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 这里进入GET方法
    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_user.count() == 1:
            t_user = t_user[0]
            t_user.Phone = t_phone
            t_user.Email = t_email
            t_user.Nickname = t_nickname
            t_user.Avator = t_avator
            t_user.Desrciption = t_description
            t_user.save()
            response['state'] = 'ok'
            response['msg'] = 'change successfully'
        else:
            response['msg'] = 'no such user'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def changePassword(request):
    # 要在登录状态下
    response = {'state':'fail', 'msg':'no msg'}

    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    if request.method != 'POST':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 获取参数
    try:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username, Password = old_password)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_user.count() <= 0:
            response['msg'] = 'username or old_password error'
        else:
            t_user = t_user[0]
            t_user.Password = new_password
            t_user.save()
            response['state'] = 'ok'
            response['msg'] = 'change successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')