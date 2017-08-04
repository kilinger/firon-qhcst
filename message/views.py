#-*- coding: utf-8 -*-
from urllib import quote
import urllib2
from django.shortcuts import render, redirect
from regist.models import Member, Educate, Occupation, Demand
from django.db.models import Q
from django.http import HttpResponse



def message_list(request):
    error = []
    openid = request.GET.get('openid', None)
    if request.GET.get('close_message', None):
        if request.session['openid']:
            del request.session['openid']
    if openid:
        request.session['openid'] = openid
        return redirect('message_list')
    else:
        try:
            openid = request.session.get('openid')
            member = Member.objects.get(openid=openid)
            if member.demand.examine != '1':
                return HttpResponse(U'您目前的状态无权查看该内容')
        except:
            host = 'http://qhcfp.xxxxx.com'
            url = '%s/message/list/' % host
            url = quote(url)
            url = 'http://zgxcw.xxxxx.com/menu.php?active=getuser&cburl=%s' % url
            return redirect(url)
    # try:
    #     if request.GET.get('openid'):
    #         openid = request.GET['openid']
    #     else:
    #         openid = request.session.get('openid')
    #     member = Member.objects.get(openid=openid)
    #     if member.demand.examine != '1':
    #         return HttpResponse(U'您目前的状态无权查看该内容')
    #     request.session['openid'] = openid
    # except:
    #     return redirect('///regist/info_basis/')

    members = Member.objects.all()
    members = members.filter(demand__examine='1')
    if request.GET.get('sort'):
        sort = request.GET.get('sort')
        identity = {
            u'创业者': 'entrepreneurs',
            u'投资人': 'investors ',
            u'其他': 'other'
        }
        if sort in identity.keys():
            sort = identity[sort]
        if sort.__len__() == 4 and int(sort) in xrange(1911):
            error = u'亲，友情提示，清华大学成立于1911年哟！'
        if sort.__len__() == 4 and int(sort) in xrange(1911, 2722):
            members = members.filter(
                Q(educate__enrol_date__year=sort) |
                Q(educate__graduate_date__year=sort)
            ).order_by('-educate__enrol_date')
        else:
            members = members.filter(
                Q(name__icontains=sort) |
                Q(identity__icontains=sort) |
                Q(trade__icontains=sort) |
                Q(educate__department__icontains=sort)
            ).distinct()
        if not members:
            error = u'对不起，没有符合搜索条件的用户！'
    return render(request, 'message_list.html', {
        'members': members,
        'error': error,
    })


def message_details(request):
    id = request.GET.get('id', None)
    try:
        member = Member.objects.get(pk=int(id))
    except:
        return HttpResponse(U'该用户已被删除')
    if member.demand.examine != '1':
        return HttpResponse(U'该用户审核状态刚刚已被修改')
    educate = Educate.objects.get(member=member)
    occupation = Occupation.objects.get(member=member)
    demand = Demand.objects.get(member=member)

    return render(request, 'message_details.html', {
        'member': member,
        'educate': educate,
        'occupation': occupation,
        'demand': demand
    })
