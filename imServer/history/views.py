from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core import serializers
import json
from account.models import User
from contact.models import Contact
from message.models import Msg
from .models import Content_Text
from .models import Content_Image
from websocket import create_connection
import time

# Create your views here.
# 返回聊天记录
def personal(request, t_username):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许GET方法
    if request.method != 'POST':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 查询的用户名为空
    if t_username == '':
        response['msg'] = 'miss username'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
   
    # 已经登录, 所以拿取用户信息
    cur_username = request.session['login_id']

    # 数据库操作,查询消息
    try:
        # 当前用户发送给对方的信息
        cur_to_t_msg = Msg.objects.filter(Username = t_username, From = cur_username)
        
        # 对方发送给当前用户的信息
        t_to_cur_msg = Msg.objects.filter(Username = cur_username, From = t_username)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        # 根据两类消息的ContentID来找出所有content
        # 这里先假设所有记录为文字类型，图片类型未知结果，待测试
        Content_Text ctArray = []
        Content_Image ciArray = []

        for msg in cur_to_t_msg:
            if msg.Type = 'text':
                ctArray.append(Content_Text.objects.filter(Cid = msg.ContentID))
            elif msg.Type = 'image':
                ciArray.append(Content_Image.objects.filter(Cid = msg.ContentID))

        for msg in t_to_cur_msg:
            if msg.Type = 'text':
                ctArray.append(Content_Text.objects.filter(Cid = msg.ContentID))
            elif msg.Type = 'image':
                ciArray.append(Content_Image.objects.filter(Cid = msg.ContentID))

        # 根据ContentID来进行append，保证时间有序
        
        if len(Content_Text) >= 1:
            # 序列化，返回多条文字内容
            serialized_obj = serializers.serialize('json', ctArray)
            response = {'state':'ok', 'msg':'ok', "data":serialized_obj}
        else:
            response['msg'] = 'no data'

    return HttpResponse(json.dumps(response), content_type = 'application/json')


# 群聊历史记录
def group(request, t_groupname):
    response = {'state':'fail', 'msg':'not defined yet'}
    return HttpResponse(json.dumps(response), content_type = 'application/json')