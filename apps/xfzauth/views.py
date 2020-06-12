from io import BytesIO

from django.contrib.auth import authenticate, get_user_model, login,logout
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_POST
from utils import restful, smssender
from utils.CCPSDK import CCPRestSDK
from utils.captcha.xfzcaptcha import Captcha
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model

User = get_user_model()

@require_POST
def login_view(request):
    form=LoginForm(request.POST)
    if form.is_valid():
        telephone=form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user=authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message='您的账号已被冻结!')
        else:
            return restful.params_error(message='您的手机号或者密码错误!')
    else:
        errors=form.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())
def img_captcha(request):
    text,image=Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out=BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    #将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    #HttpResponse默认存储字符串,现在改为图片png格式
    response=HttpResponse(content_type='image/png')

    #从BytesIO的管道中,读取图片数据,保存到response对象中
    response.write(out.read())
    # out.tell()--获取当前文件指针的位置--即告诉文件的大小
    response['Content-length'] = out.tell()
    # 设置memcahed
    cache.set(text.lower(), text.lower(), 5 * 60)
    return response

# 容联云短信验证码
# def sms_captcha(request):
#
#     #/smscode?tel=xxxx
#     telephone=request.GET.get("telephone")
#     accountSid="8aaf07087249953401727c857d61199f"
#     accoundToken="7936c612923948e0b4844e47c2168352"
#     appId="8aaf07087249953401727c857e8519a5"
#     rest=CCPRestSDK.REST(accountSid,accoundToken,appId)
#     result=rest.sendTemplateSMS(telephone,["1234"],"1")
#
#     print("="*30)
#     print(result)
#     print("="*30)
#
#     return restful.ok()

def sms_captcha(request):
    # /sms_captcha/?telephone=xxx
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone,code,5*60)
    print('短信验证码：',code)
    # result = aliyunsms.send_sms(telephone,code)
    result = smssender.send(telephone,code)
    if result:
        return restful.ok()
    else:
        return result.params_error(message="短信验证码发送失败！")










