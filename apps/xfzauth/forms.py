from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,error_messages={'max_lenth':'手机长度为11位'})
    password = forms.CharField(max_length=20,min_length=6,error_messages={"max_length":"密码最多不能超过20个字符！","min_length":"密码最少不能少于6个字符！"})
    remember = forms.IntegerField(required=False)
class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6,
                               error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！"})
    password2 = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！"})
    img_captcha = forms.CharField(min_length=4,max_length=4)
    # 短信验证码有些问题,没有采取memcached存储
    sms_captcha = forms.CharField(min_length=4,max_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        # 验证两次密码输入是否一致
        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')
        # 图片验证码
        img_captcha = cleaned_data.get('img_captcha')
        #是否存储在memcache 中
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError("图形验证码错误！")
        # 获取电话号码
        telephone = cleaned_data.get('telephone')
        # 图片验证码和短信验证码都是用来验证是否是人为操作
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)

        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        # 检测数据库是否存在有该号码,若有则此账号已被注册
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            forms.ValidationError('该手机号码已经被注册！')

        return cleaned_data
