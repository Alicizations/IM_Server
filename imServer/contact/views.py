# from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from account.models import User
from .models import Contact
# from content.models import Content_AddMsg
# from message.models import Msg

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
        if t_contact.count() <= 0:
            response['state'] = 'ok'
            response['msg'] = 'no friend'
        else:
            temp = []
            for x in t_contact:
                temp.append(model_to_dict(x))
            response = {'state':'ok', 'msg':'friends', "data":temp}

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def add(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许POST操作
    if request.method != 'POST':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 获取参数, cid == 0 则是申请添加; cid > 0则是同意添加, 需要查询数据库
    try:
        r_username = request.POST['username']
        # r_cid = request.POST['cid']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # if cid == 0:
        

    # 数据库操作
    try:
        t_user = User.objects.filter(Username = r_username)
        t_contact = Contact.objects.filter(Username = t_username, Friend = r_username)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_user.count() <= 0:
            response['msg'] = 'user does not exist'
        elif t_contact.count() > 0:
            response['msg'] = 'already exist'
        else:
            Contact.objects.create(
                Username = t_username,
                Friend = r_username
            )
            Contact.objects.create(
                Username = r_username,
                Friend = t_username
            )
            response['state'] = 'ok'
            response['msg'] = 'add friends successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')



def delete(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许POST操作
    if request.method != 'POST':
        response['msg'] = 'wrong method'
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
        t_contact_t = Contact.objects.filter(Username = t_username, Friend = r_username)
        t_contact_r = Contact.objects.filter(Username = r_username, Friend = t_username)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_contact_t.count() <= 0 and t_contact_r.count() <= 0:
            response['msg'] = 'no such relationship'
        elif t_contact_t.count() > 0:
            t_contact_t = t_contact_t[0]
            t_contact_t.delete()
            response['state'] = 'ok'
            response['msg'] = 'delete friends successfully'
        elif t_contact_r.count() > 0:
            t_contact_r = t_contact_r[0]
            t_contact_r.delete()
            response['state'] = 'ok'
            response['msg'] = 'delete friends successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')