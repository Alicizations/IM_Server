# from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from account.models import User
from .models import Contact

# Create your views here.

def info(request):
    response = {'state':'fail', 'msg':'no msg', 'data':[]}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 只允许GET方法获得好友列表
    if request.method != 'GET':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 这里进入GET方法
    # 数据库操作
    try:
        t_contact = Contact.objects.filter(Username = t_username)

    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_contact.count() == 1:
            t_contact = t_contact[0]
            t_friends = t_contact.Friends
            # 处理字符串,获取好友
            friends = t_friends.spilt()
            for friend_ID in friends_str:
                try:
                    t_user = User.objects.filter(UserID = friend_ID)
                except Exception as e:
                    response['msg'] = 'db error'
                    return HttpResponse(json.dumps(response), content_type = 'application/json')
                response['data'].append(t_user)
            response['state'] = 'ok'
            response['msg'] = 'get successfully'
        else:
            response['msg'] = 'no such user'

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def add(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 获取参数
    try:
        r_username = request.POST['username']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = r_username)
        t_contact = Contact.objects.filter(Username = t_username)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_user.count() <= 0:
            response['msg'] = 'user does not exist'
        else:
            t_contact.Friends = str(t_contact.Friends) + ',' + t_user.UserID
            response['state'] = 'ok'
            response['msg'] = 'add friends successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')



def delete(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 获取参数
    try:
        r_username = request.POST['username']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = r_username)
        t_contact = Contact.objects.filter(Username = t_username)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        # 解析contact里面的字符串
        friends_strs = t_contact.Friends.split()
        # 未添加该好友
        if str(t_user.UserID) not in friends_strs:
            response['msg'] = 'user does not exist'
        else:
            friends_strs.remove(str(t_user.UserID))
            friends = ','.join(friends_strs)
            t_contact.Friends = friends
            response['state'] = 'ok'
            response['msg'] = 'delete friends successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')