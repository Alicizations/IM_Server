from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from account.models import User
from contact.models import Contact
from message.models import Msg
from .models import Content_Text
from .models import Content_Image
from .models import Content_AddMsg
from websocket import create_connection
import time


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

    seq = checkSeqByUsername(to_username)

    # seq 错误处理
    if seq == -1:
        return jsonMSG(msg = 'get seq fail')

    # 数据库操作,插入消息,并插入到message
    try:
        Content_Text.objects.create(
            Cid = cid,
            Cstr = t_data,
            Timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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

    seq = checkSeqByUsername(to_username)
    # seq 错误处理
    if seq == -1:
        return jsonMSG(msg = 'get seq fail')

    # 数据库操作,插入图片
    try:
        Content_Image.objects.create(
            Cid = cid,
            Cimage = "img/"+ t_data.name,
            Timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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

def jsonMSG(state = 'fail', msg = 'no msg', data = []):
    response = {'state':state, 'msg':msg, 'data':data}
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
    # ws = create_connection('ws://118.89.65.154:6789')
    ws = create_connection('ws://172.18.32.97:6789')

    msg = {'action': 'new', 'data': username}
    print('Sending msg to User ' + username)
    ws.send(json.dumps(msg))

    result =  ws.recv()
    print('Received: %s' % result)

    ws.close()

def add(request):
    # 要在登录状态下
    if 'login_id' not in request.session:
        return jsonMSG(msg = 'no login')

    # 只允许POST方法
    if request.method != 'POST':
        return jsonMSG(msg = 'wrong method')
    
    # 已经登录, 所以拿取用户信息
    from_username = request.session['login_id']

    # 获取参数, cid == 0 则是申请添加; cid > 0则是同意添加, 需要查询数据库
    try:
        to_username = request.POST['to']
        to_cid = request.POST['cid']
        to_cid = int(to_cid)
        t_info = request.POST['info']
    except Exception as e:
        return jsonMSG(msg = 'POST parameter error')

    # 查询用户是否存在
    try:
        t_user = User.objects.filter(Username = to_username)
    except Exception as e:
        return jsonMSG(msg = 'db error')
    else:
        # 查询不到该用户, 申请失败
        if t_user.count() <= 0:
            return jsonMSG(msg = 'no such user')

    # 好友申请
    if to_cid <= 0:
        # 创建申请信息
        # 创建 content_add 信息
        # 在 user 的 messageTable 添加信息
        # websocket 通知用户
        try:
            seq = checkSeqByUsername(to_username)
            # seq 错误处理
            if seq == -1:
                return jsonMSG(msg = 'get seq fail')
            Content_AddMsg.objects.create(
                From = from_username,
                To = to_username,
                Info = t_info,
                Timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            Msg.objects.create(
                Username = to_username,
                Seq = seq,
                From = from_username,
                Type = 'addRequest',
                ContentID = cid
            )
        except Exception as e:
            return jsonMSG(msg = 'db error when add request')
        else:
            # 用websocket告知用户有新消息
            tellUserReceiveMessage(to_username)
            return jsonMSG(state = 'ok', msg = 'send request successfully')

    # cid > 0, 为同意申请
    else:
        try:
            t_addRequest = Content_AddMsg.objects.filter(Cid = to_cid)
        except Exception as e:
            return jsonMSG(msg = 'db error when check request')
        else:
            if t_addRequest.count() <= 0:
                return jsonMSG(msg = 'no such request')
            else:
                t_addRequest = t_addRequest[0]
                # 如果查询到的请求不符合, 则返回错误
                if t_addRequest.From != to_username or t_addRequest.To != from_username:
                    return jsonMSG(msg = 'inconformity')
                # 请求符合, 添加为好友
                else:
                    try:
                        seq = checkSeqByUsername(from_username)
                        # seq 错误处理
                        if seq == -1:
                            return jsonMSG(msg = 'get seq fail')
                        r_contact = Contact.objects.filter(Username = from_username, Friend = to_username)
                        if r_contact.count() <= 0:
                            Contact.objects.create(
                                Username = from_username,
                                Friend = to_username
                            )
                        r_contact = Contact.objects.filter(Username = to_username, Friend = from_username)
                        if r_contact.count() <= 0:
                            Contact.objects.create(
                                Username = to_username,
                                Friend = from_username
                            )
                        Msg.objects.create(
                            Username = from_username,
                            Seq = seq,
                            From = to_username,
                            Type = 'addComfirm',
                            ContentID = 0
                        )
                        tellUserReceiveMessage(from_username)
                    except Exception as e:
                        return jsonMSG(msg = 'db or websocket error when add contact')
                    else:
                        return jsonMSG(state = 'ok', msg = 'add contact successfully')
    return jsonMSG(msg = 'some thing wrong')


def checkSeqByUsername(username):
    seq = 1
    # 处理seq, 在Msg根据接收方用户名找到上一个seq, 若不存在则初始化为1
    try:
        t_msg = Msg.objects.filter(Username = username)
    except Exception as e:
        return -1
    else:
        # 找到该用户最大的seq
        if t_msg.count() > 0:
            seq = t_msg.count() + 1

    return seq