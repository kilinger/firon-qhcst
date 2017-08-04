#-*- coding: utf-8 -*-
from urllib import quote, unquote
from django.shortcuts import render, redirect
from regist.forms import RegistOccupationForm, RegistDemandForm, RegistEducateForm, RegistBasisForm, BasisForm
from regist.models import Member, Educate, Occupation, Demand
from member.utils import iframe_jsonify


def regist_index(request):
    return render(request, 'regist_index.html', {})


def regist_info_basis(request):
    openid = []
    headurl = []
    host = 'http://qhcfp.xxxxx.com'
    url = '%s/regist/info_basis/?pre=up' % host
    url = quote(url)
    url = 'http://zgxcw.xxxxx.com/menu.php?active=getuser&cburl=%s' % url
    if request.GET.get('openid'):
        openid = request.GET.get('openid')
        get = dict(request.GET)
        if get.has_key('headurl'):
            headurl = True
            image = request.GET.get('headurl')
            image = unquote(image)
            wechat = {'openid': openid, 'image': image}
            request.session['wechat'] = wechat

    if request.method == 'POST':
        form = RegistBasisForm(request.POST)
        if request.is_ajax():
            basis = request.POST
            basis = dict(basis)
            for k, v in basis.iteritems():
                basis[k] = v[0]
            request.session['basis'] = basis
            return iframe_jsonify(state=True, url=url)

        if form.is_valid():
            basis = form.cleaned_data
            request.session['basis'] = basis
            return redirect('///regist/info_educate/?pre=up')
    else:
        form = RegistBasisForm()
        if request.GET.get('pre') == 'up':
            basis = request.session.get('basis')
            form = RegistBasisForm(initial=basis)
    return render(request, 'regist_info_basis.html', {
        'form': form,
        'openid': openid,
        'headurl': headurl,
    })


def edit_info_basis(request):
    id = request.session.get('member_id')
    basis = Member.objects.get(pk=id)
    form = BasisForm(instance=basis)
    if request.method == 'POST':
        form = BasisForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data
            Member.objects.filter(pk=id).update(**date)
            return redirect('regist_info_preview')
    return render(request, 'regist_info_basis.html', {
        'form': form,
    })


def regist_info_educate(request):
    if request.method == 'POST':
        form = RegistEducateForm(request.POST)
        if form.is_valid():
            educate = form.cleaned_data
            request.session['educate'] = educate
            return redirect('///regist/info_occupation/?pre=up')
    else:
        form = RegistEducateForm()
        if request.GET.get('pre') == 'up':
            educate = request.session.get('educate')
            form = RegistEducateForm(initial=educate)
    return render(request, 'regist_info_educate.html', {
        'form': form,
        'pre': 'up',
    })


def edit_info_educate(request):
    second = False
    id = request.session.get('member_id')
    educate = Educate.objects.get(member__id=id)
    if educate.second_graduate_date and educate.second_enrol_date and educate.second_degree and educate.second_school and educate.second_department:
        second = True
    form = RegistEducateForm(instance=educate)
    if request.method == 'POST':
        form = RegistEducateForm(request.POST)
        if form.is_valid():
            educate = form.cleaned_data
            member = Member.objects.get(pk=id)
            Educate.objects.filter(member=member).update(**educate)
            return redirect('regist_info_preview')
    return render(request, 'regist_info_educate.html', {
        'form': form,
        'second': second,
    })


def regist_info_occupation(request):
    id = request.session.get('member_id')
    if request.method == 'POST':
        form = RegistOccupationForm(request.POST)
        if form.is_valid():
            occupation = form.cleaned_data
            request.session['occupation'] = occupation
            return redirect('///regist/info_demand/?pre=up')
    else:
        form = RegistOccupationForm()
        if request.GET.get('pre') == 'up':
            occupation = request.session.get('occupation')
            form = RegistOccupationForm(initial=occupation)
    return render(request, 'regist_info_occupation.html', {
        'form': form,
        'pre': 'up',
    })


def edit_info_occupation(request):
    id = request.session.get('member_id')
    occupation = Occupation.objects.get(member=id)
    form = RegistOccupationForm(instance=occupation)
    if request.method == 'POST':
        form = RegistOccupationForm(request.POST)
        if form.is_valid():
            occupation = form.cleaned_data
            member = Member.objects.get(pk=id)
            Occupation.objects.filter(member=member).update(**occupation)
            return redirect('regist_info_preview')
    return render(request, 'regist_info_occupation.html', {
        'form': form,
    })


def regist_info_demand(request):
    if request.method == 'POST':
        form = RegistDemandForm(request.POST)
        if form.is_valid():
            demand = form.cleaned_data
            request.session['demand'] = demand
            basis = request.session.get('basis')
            wechat = request.session.get('wechat')
            if wechat:
                basis = dict(basis, **wechat)
            educate = request.session.get('educate')
            occupation = request.session.get('occupation')
            demand = request.session.get('demand')

            member = Member.objects.create(**basis)
            request.session['member_id'] = member.id
            id = request.session.get('member_id')
            member = Member.objects.get(pk=id)
            Educate.objects.filter(member=member).update(**educate)
            Occupation.objects.filter(member=member).update(**occupation)
            Demand.objects.filter(member=member).update(**demand)

            up_member = Member.objects.filter(**basis)
            if len(up_member) > 1:
                for num in xrange(1, len(up_member)):
                    up_member[num].delete()
            return redirect('regist_info_preview')
    else:
        form = RegistDemandForm()
        if request.GET.get('pre') == 'up':
            demand = request.session.get('demand')
            form = RegistDemandForm(initial=demand)
    return render(request, 'regist_info_demand.html', {
        'form': form,
        'pre': 'up',
    })


def edit_info_demand(request):
    id = request.session.get('member_id')
    demand = Demand.objects.get(member__id=id)
    form = RegistDemandForm(instance=demand)
    if request.method == 'POST':
        form = RegistDemandForm(request.POST)
        if form.is_valid():
            demand = form.cleaned_data
            member = Member.objects.get(pk=id)
            edit = Demand.objects.get(member=member)
            edit.demand = demand['demand']
            edit.supply = demand['supply']
            edit.save()
            return redirect('regist_info_preview')
    return render(request, 'regist_info_demand.html', {
        'form': form,
    })


def regist_info_preview(request):
    try:
        del request.session['basis']
        del request.session['educate']
        del request.session['occupation']
        del request.session['demand']
        del request.session['wechat']
    except:
        pass
    if request.GET.get('openid'):
        openid = request.GET.get('openid')
        basis = Member.objects.get(openid=openid)
        id = basis.id
    else:
        id = request.session.get('member_id')
        basis = Member.objects.get(pk=id)
    educate = Educate.objects.get(member__id=id)
    occupation = Occupation.objects.get(member__id=id)
    demand = Demand.objects.get(member__id=id)
    if request.method == 'POST':
        return redirect('regist_finish')
    request.session['member_id'] = basis.id
    return render(request, 'regist_info_preview.html', {
        'basis': basis,
        'educate': educate,
        'occupation': occupation,
        'demand': demand,
        })


def regist_finish(request):
    try:
        del request.session['member_id']
    except:
        pass
    return render(request, 'finish.html')
