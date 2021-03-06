# from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from django.conf import settings
from .models import User
from content.views import jsonMSG
import os
from django.http import QueryDict
from message.models import UserSeq


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
            temp = User.objects.create(
                Username = t_username,
                Password = t_password
            )
            UserSeq.objects.create(
                User = temp
            )
            response['state'] = 'ok'
            response['msg'] = 'register successfully'
        else:
            response['msg'] = 'repeat username'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def logout(request):
    response = {'state':'fail', 'msg':'no msg'}
    # 只允许通过 DELETE 方法退出登录
    if request.method != 'DELETE':
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

def uploadAvatar(request):

    # if request.method == 'GET':
    #     t_user = User.objects.filter(Username = '123')
    #     t_user = t_user[0]
    #     return jsonMSG(msg = 'upload successfully', data = t_user.Avatar.url)
    
    # 要在登录状态下
    if 'login_id' not in request.session:
        return jsonMSG(msg = 'no login')

    if request.method != 'POST':
        return jsonMSG(msg = 'wrong method')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']
    # t_username = '123'

    print(request.FILES)
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        return jsonMSG(msg = 'db error')
    else:
        if t_user.count() <= 0:
            return jsonMSG(msg = 'no such user')
        else:
            t_user = t_user[0]
            removeOldAvatar(t_user.Avatar.url)
            t_user.Avatar = request.FILES['file']
            t_user.save()
            return jsonMSG(state = 'ok', msg = t_user.Avatar.url)
    return jsonMSG(msg = 'invalid form')

def removeOldAvatar(url):

    print(url)

    if url == '/media/avatar/default.png':
        return

    # filePath = os.path.join(settings.BASE_DIR, url).replace('\\', '/')
    filePath = settings.BASE_DIR.replace('\\', '/') + url
    print(filePath)

    try:
        os.remove(filePath)
    except Exception as e:
        print('remove file error:')
        print(e)

def info(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    if request.method == 'PUT':
        # 获取参数
        try:
            t_phone = request.PUT['phone']
            t_email = request.PUT['email']
            t_nickname = request.PUT['nickname']
            t_avatar = request.PUT['avatar']
            t_description = request.PUT['description']
        except Exception as e:
            response['msg'] = 'PUT parameter error'
            return HttpResponse(json.dumps(response), content_type = 'application/json')

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
                t_user.Description = t_description
                t_user.save()
                response['state'] = 'ok'
                response['msg'] = 'change successfully'
            else:
                response['msg'] = 'no such user'

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
            # temp = model_to_dict(t_user[0])
            t_user = t_user[0]
            temp = {}
            temp['Username'] = t_user.Username
            temp['Gender'] = t_user.Gender
            temp['Region'] = t_user.Region
            temp['Nickname'] = t_user.Nickname
            temp['Avatar'] = t_user.Avatar.url
            temp['Description'] = t_user.Description
            
            response = {'state':'ok', 'msg':'ok', "data":temp}
        else:
            response['msg'] = 'no data'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def othersInfo(request, t_username):
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
            temp = {}
            temp['Username'] = t_user.Username
            temp['Gender'] = t_user.Gender
            temp['Region'] = t_user.Region
            temp['Nickname'] = t_user.Nickname
            temp['Avatar'] = t_user.Avatar.url
            temp['Description'] = t_user.Description
            response = {'state':'ok', 'msg':'ok', "data":temp}
        else:
            response['msg'] = 'no data'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def changePassword(request):
    # 要在登录状态下
    response = {'state':'fail', 'msg':'no msg'}

    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    if request.method != 'PUT':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 获取参数
    try:
        old_password = request.PUT['old_password']
        new_password = request.PUT['new_password']
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

def changeInfo(request, t_attr):

    # 要在登录状态下
    if 'login_id' not in request.session:
        return jsonMSG(msg = 'no login')

    if request.method != 'PUT':
        return jsonMSG(msg = 'wrong method')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # print(request.body)

    put = QueryDict(request.body)

    # 获取参数
    try:
        # t_value = request.PUT['value']
        t_value = put.get('value')
    except Exception as e:
        return jsonMSG(msg = 'PUT parameter error')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        return jsonMSG(msg = 'db error')
    else:
        if t_user.count() <= 0:
            return jsonMSG(msg = 'no such user')
        else:
            t_user = t_user[0]
            if t_attr == 'Password':
                t_user.Password = t_value
                t_user.save()
            elif t_attr == 'Gender':
                t_user.Gender = t_value
                t_user.save()
            elif t_attr == 'Region':
                t_user.Region = t_value
                t_user.save()
            elif t_attr == 'Nickname':
                t_user.Nickname = t_value
                t_user.save()
            elif t_attr == 'Description':
                t_user.Description = t_value
                t_user.save()
            

    return jsonMSG(state = 'ok', msg = 'change successfully')

def getUser(t_username):
    
    if type(t_username) != type('1'):
        return None, 'type error'

    # 查询用户
    try:
        t_user = User.objects.filter(Username = t_username)
    except Exception as e:
        return None, 'db error when get user'
    else:
        if t_user.count() == 1:
            return t_user[0], None 
        return None, 'no such user'

    return None, 'fail'