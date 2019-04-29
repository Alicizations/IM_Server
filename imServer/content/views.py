from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from account.models import User
from contact.models import Contact
from .models import Content_Text
from .models import Content_Image


# Create your views here.
# 上传一个string，只允许post方法
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
    
    # 获取参数
    try:
        t_data = request.POST['data']
        t_username = request.POST['to']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 此处未创建message表格，暂未实现插入到message


    # 为消息设定一个id，这里使用的是消息表的长度+1
    cid = len(Content_Text.objects.all()) + 1

    # 数据库操作,插入消息
    try:
        Content_Text.objects.create(
            Cid = cid,
            Cstr = t_data
        )
        response['state'] = 'ok'
        response['msg'] = 'send successfully'
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
    
    # 获取参数
    try:
        t_data = request.POST['data']
        t_username = request.POST['to']
    except Exception as e:
        response['msg'] = 'POST parameter error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')

    # 此处未创建message表格，暂未实现插入到message
    

    # 为消息设定一个id，这里使用的是消息表的长度+1
    cid = len(Content_Image.objects.all()) + 1

    # 图片如何转换到存储格式，暂未实现

    # 数据库操作,插入图片
    try:
        Content_Image.objects.create(
            Cid = cid,
            Cimage = t_data
        )
        response['state'] = 'ok'
        response['msg'] = 'send successfully'
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
        # 此处是否需要实现，存储格式转换成图片再返回，待实现
        
        
    except Exception as e:
        response['msg'] = 'db error'
        return HttpResponse(json.dumps(response), content_type = 'application/json')
    else:
        if t_image.count() == 1:
            temp = model_to_dict(t_image[0])
            response = {'state':'ok', 'msg':'ok', "data":temp}
        else:
            response['msg'] = 'no data'

    return HttpResponse(json.dumps(response), content_type = 'application/json')
