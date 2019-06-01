from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from .models import Msg
from content.models import Content_Text
from content.models import Content_Image
from content.models import Content_AddMsg
from content.views import jsonMSG
from account.views import getUser

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
            # 返回具体信息
            for index in range(t_msg.count()):
                msg_entry = t_msg[index]
                msg_dict = model_to_dict(msg_entry)
                msg_dict['content'] = getContentAndTimeByTypeAndCid(msg_entry.Type, msg_entry.ContentID)
                temp.append(msg_dict)

            response = {'state':'ok', 'msg':'ok', "data":temp}

            response['state'] = 'ok'
            response['msg'] = 'get message successfully'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

# 根据类型和cid获取具体的content返回
# 如果返回空(''), 代表存在异常或数据不存在
def getContentAndTimeByTypeAndCid(msg_type, msg_cid):
    # 简单错误处理
    if msg_cid <= 0:
        return ''

    if msg_type == 'text':
        try:
            t_content = Content_Text.objects.filter(Cid = msg_cid)
        except Exception as e:
            print('msg return text db error: ', e)
            return ''
        else:
            if t_content.count() <= 0:
                return ''
            else:
                return model_to_dict(t_content[0])
        
    elif msg_type == 'image':
        try:
            t_content = Content_Image.objects.filter(Cid = msg_cid)
        except Exception as e:
            print('msg return image db  error: ', e)
            return ''
        else:
            if t_content.count() <= 0:
                return ''
            else:
                t_c = t_content[0]
                temp = {}
                temp['Cid'] = t_c.Cid
                temp['Cstr'] = t_c.Cimage.url
                temp['Timestamp'] = t_c.Timestamp
                # return model_to_dict(t_content[0])
                return temp

    elif msg_type == 'addRequest':
        try:
            t_content = Content_AddMsg.objects.filter(Cid = msg_cid)
        except Exception as e:
            return ''
        else:
            t_c = t_content[0]
            temp = {}
            temp['Cid'] = t_c.Cid
            temp['Cstr'] = t_c.Info
            temp['Timestamp'] = t_c.Timestamp
            # return model_to_dict(t_content[0])
            return temp

    else:
        return ''

def seq(request):
    # 要在登录状态下
    if 'login_id' not in request.session:
        return jsonMSG(msg = 'no login')

    # 已经登录, 所以拿取用户信息
    t_username = request.session['login_id']

    # GET 方法
    # 获取保存在数据库的 seq
    if request.method == 'GET':
        t_user, err = getUser(t_username)
        if err:
            return jsonMSG(msg = err)

        return jsonMSG(state = 'ok', msg = 'get', data = t_user.seq.all()[0].Seq)

    # POST 方法
    # 更新数据库的 seq
    if request.method == 'POST':
        t_user, err = getUser(t_username)
        if err:
            return jsonMSG(msg = err)

        try:
            t_seq = request.POST['seq']
            t_s = t_user.seq.all()[0]
            t_s.Seq = t_seq
            t_s.save()
        except Exception as e:
            return jsonMSG(msg = 'modify fail')

        return jsonMSG(state = 'ok', msg = 'succeed')

    return jsonMSG(msg = 'wrong method')