from django.core.cache import cache

from user.models import User
from common import errors
from lib.http import render_json
from lib.sms import send_vcode
from common import keys


# Create your views here.
def submit_phonenum(request):
    """提交手机号码"""
    phone = request.POST.get('phone')
    if phone:
        result, msg = send_vcode(phone)
        if result:
            return render_json(code=0, data=msg)
        else:
            return render_json(code=errors.SMS_ERROR, data=msg)
    else:
        return render_json(code=errors.PhoneNum_Empty, data='手机号码不能为空')


def submit_vcode(request):
    """提交短信验证码"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中取出vcode
    cached_vcode = cache.get(keys.VCODE_KEY % phone)
    if cached_vcode == vcode:
        # 验证码正确,可以登录或者注册.
        # try:
        #     user = User.objects.get(phonenum=phone)
        #     # 登录
        # except User.DoesNotExist:
        #     # 注册
        #     User.objects.create(phonenum=phone, nickname=phone)

        # 使用User.objects.get_or_create()来简化
        user, created = User.objects.get_or_create(phonenum=phone, nickname=phone)
        request.session['uid'] = user.id
        return render_json(code=0, data=user.to_dict())
    else:
        # 验证不正确
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


# def (request):
#     """获取个人资料"""
#     pass
#
# def (request):
#     """修改个人资料"""
#     pass
#
# def (request):
#     """头像上传"""
#     pass


