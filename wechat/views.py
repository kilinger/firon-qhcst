# -*- coding: utf-8 -*-
import random
import hashlib
from urllib import unquote
import urllib2
from member.utils import iframe_jsonify
from regist.models import Member


def openid(request):
    openid = request.GET.get('openid')
    member = Member.objects.all()
    member = member.filter(openid=openid)
    if member:
        member = member[0]
        examine = member.demand.examine
        return iframe_jsonify(regist=True, examine=examine)
    else:
        return iframe_jsonify(regist=False, examine=None)


def verification_code(request):
    phone = request.GET.get('phone')
    member = Member.objects.all().filter(mobile_phone=phone)
    if member:
        member = member[0]
        mobile = str(member.mobile_phone)
        account = 'cf_chuanshiyun'
        password = str(hashlib.md5('wly.1234').hexdigest())
        code = str(random.random()).split('.')[-1][4:8]
        content = '感谢您关注清华俱乐部，验证码为【%s】，10分钟内有效。' % code
        url = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit&account=%s&password=%s&mobile=%s&content=%s' % (account, password, mobile, content)
        urllib2.urlopen(url)
        id = member.id
        return iframe_jsonify(regist=True, data=code, id=id)
    else:
        return iframe_jsonify(regist=False, data=u'', id=u'')


def bind(request):
    id = request.GET.get('id')
    openid = request.GET.get('openid')
    member = Member.objects.filter(id=id)
    if member:
        member = member[0]
        member.openid = openid
        image = request.GET.get('headurl')
        image = unquote(image)
        member.image = image
        member.save()
        return iframe_jsonify(data=True)
    else:
        return iframe_jsonify(data=False)
