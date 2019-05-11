from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from account.models import User
from contact.models import Contact
from message.models import Msg
from .models import Content_Text
from .models import Content_Image
from websocket import create_connection


# Create your views here.
# 上传一个string, 只允许post方法
def text(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许POST方法
    if request.method != 'POST':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    
    # 已经登录, 所以拿取用户信息
    from_username = request.session['login_id']

    # 获取参数
    try:
        t_data = request.POST['data']
        to_username = request.POST['to']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    if not checkRelationship(from_username, to_username):
        return jsonMSG(msg = 'you are not friends!')

    # 为消息设定一个id, 这里使用的是消息表的长度+1
    cid = len(Content_Text.objects.all()) + 1

    seq = 1
    # 处理seq, 在Msg根据接收方用户名找到上一个seq, 若不存在则初始化为1
    try:
        t_msg = Msg.objects.filter(Username = to_username)

    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        # 找到该用户最大的seq
        if t_msg.count() > 0:
            for msg in t_msg:
                seq = max(seq, msg.Seq)
            seq += 1

    # 数据库操作,插入消息,并插入到message
    try:
        Content_Text.objects.create(
            Cid = cid,
            Cstr = t_data
        )
        Msg.objects.create(
            Username = to_username,
            Seq = seq,
            From = from_username,
            Type = 'text',
            ContentID = cid
        )
        response['state'] = 'ok'
        response['msg'] = 'send successfully'

        # 用websocket即时告知用户有新消息
        tellUserReceiveMessage(to_username)
        
    except Exception as e:
        response['msg'] = 'db error'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def image(request):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许POST方法
    if request.method != 'POST':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    
    # 已经登录, 所以拿取用户信息
    from_username = request.session['login_id']

    # 获取参数
    try:
        t_data = request.POST['data']
        to_username = request.POST['to']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    if not checkRelationship(from_username, to_username):
        return jsonMSG(msg = 'you are not friends!')

    # 为消息设定一个id, 这里使用的是消息表的长度+1
    cid = len(Content_Image.objects.all()) + 1

    seq = 1
    # 处理seq, 在Msg根据接收方用户名找到上一个seq, 若不存在则初始化为1
    try:
        t_msg = Msg.objects.filter(Username = to_username)

    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        # 找到该用户最大的seq
        if t_msg.count() > 0:
            for msg in t_msg:
                seq = max(seq, msg.Seq)
            seq += 1

    # 数据库操作,插入图片
    try:
        Content_Image.objects.create(
            Cid = cid,
            Cimage = "img/"+ t_data.name
        )
        Msg.objects.create(
            Username = to_username,
            Seq = seq,
            From = from_username,
            Type = 'image',
            ContentID = cid
        )
        
        # 保存文件
        fname = settings.MEDIA_ROOT + "/img/" + f1.name
        with open(fname,'wb') as pic:
            for c in f1.chunks():
                pic.write(c)

        response['state'] = 'ok'
        response['msg'] = 'send successfully'

        # 用websocket即时告知用户有新消息
        tellUserReceiveMessage(to_username)

    except Exception as e:
        response['msg'] = 'db error'

    return HttpResponse(json.dumps(response), content_type = 'application/json')



def text_detail(request, text_id):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许GET方法
    if request.method != 'GET':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    
    # 数据库操作,查询消息
    try:
        t_text = Content_Text.objects.filter(Cid = text_id)
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_text.count() == 1:
            temp = model_to_dict(t_text[0])
            response = {'state':'ok', 'msg':'ok', "data":temp}
        else:
            response['msg'] = 'no data'

    return HttpResponse(json.dumps(response), content_type = 'application/json')


def image_detail(request, image_id):
    response = {'state':'fail', 'msg':'no msg'}

    # 要在登录状态下
    if 'login_id' not in request.session:
        response['msg'] = 'no login'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 只允许GET方法
    if request.method != 'GET':
        response['msg'] = 'wrong method'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    
    # 数据库操作,查询消息
    try:
        t_image = Content_Image.objects.filter(Cid = image_id)
        
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_image.count() == 1:
            temp = model_to_dict(t_image[0].Cimage)
            response = {'state':'ok', 'msg':'ok', "data":temp}
        else:
            response['msg'] = 'no data'

    return HttpResponse(json.dumps(response), content_type = 'application/json')

def jsonMSG(state = 'fail', msg = 'no msg'):
    response = {'state':state, 'msg':msg, 'data':[]}
    return HttpResponse(json.dumps(response), content_type = 'application/json')

def checkRelationship(user_now, user_target):

    # 在联系人表查找是否存在两人的好友关系
    try:
        t_contact = Contact.objects.filter(Username = user_now, Friend = user_target)
    except Exception as e:
        print(e)
        return False
    else:
        if t_contact.count() <= 0:
            return False
        else:
            return True
    
    return False

def tellUserReceiveMessage(username):
    ws = create_connection('ws://118.89.65.154:6789')

    msg = {'action': 'new', 'data': username}
    print('Sending msg to User ' + username)
    ws.send(json.dumps(msg))

    result =  ws.recv()
    print('Received: %s' % result)

    ws.close()