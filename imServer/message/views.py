from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from .models import Msg

def messageTable(request, seq):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只接受 GET 请求
    if request.method != 'GET':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # 数据库操作
    try:
        t_msg = Msg.objects.filter(Username = t_username, Seq__gt = seq)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_msg.count() <= 0:
            response['msg'] = 'no data'
        else:
            temp = []
            for index in range(t_msg.count()):
                temp.append(model_to_dict(t_user[index]))

            response = {'state':'ok', 'msg':'ok', "data":temp}

            response['state'] = 'ok'
            response['msg'] = 'get message successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')