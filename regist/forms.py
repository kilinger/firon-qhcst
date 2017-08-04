#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
import datetime
from regist.models import Member, Occupation, Demand, Educate


class BasisForm(forms.ModelForm):
    SEX_CHOICES = (
        ('w', _(u'女')),
        ('m', _(u'男')),
    )
    INDENTITY_CHOICES = (
        ('entrepreneurs', _(u'创业者')),
        ('investors ', _(u'投资人')),
        ('other', _(u'其他')),
    )
    name = forms.CharField(max_length=8, label=_(u'姓名'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={"id": "sex"}), choices=SEX_CHOICES, label=_(u'性别'))
    identity = forms.ChoiceField(widget=forms.RadioSelect(attrs={"id": "identity"}), choices=INDENTITY_CHOICES, label=_(u'身份'))
    company = forms.CharField(label=_(u'公司'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    job = forms.CharField(label=_(u'职位'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    email = forms.EmailField(label=_(u'邮箱'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    mobile_phone = forms.CharField(label=_(u'手机'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    trade = forms.CharField(label=_(u'行业'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    city = forms.CharField(label=_(u'城市'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    # wechat = forms.CharField(label=_(u'微信'), required=False, widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    openid = forms.CharField(label=_(u'微信id'), required=False)
    image = forms.URLField(label=_(u'微信头像'), required=False)

    class Meta:
        model = Member
        exclude = ('email',)

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if mobile_phone:
            def length(string):
                if not isinstance(string, unicode):
                    string = string.decode('utf-8')
                count = 0
                for c in string:
                    if u'\u0100' < c < u'\uffff':
                        count += 2
                    else:
                        count += 1
                return count
            try:
                int(mobile_phone)
            except:
                raise forms.ValidationError(_(u'请填写整数'))
            if length(mobile_phone) != 11:
                raise forms.ValidationError(_(u'请输入正确的手机号！'))
            if mobile_phone[0] != '1':
                raise forms.ValidationError(_(u'第一位必须为1！'))
            return mobile_phone
        else:
            return mobile_phone

    def clean(self):
        # form = super(RegistBasisForm, self).clean()
        form = self.cleaned_data
        keys = form.keys()
        for key in keys:
            if key == 'openid' or key == 'image' or key == 'wechat':
               pass
            else:
                if form[key].strip() == u'':
                    msg = u'请不要输入空格！'
                    self._errors[key] = self.error_class([msg])
        return form

    def clean_trade(self):
        data = self.cleaned_data
        trade = data.get('trade')
        if len(trade) > 8:
            raise forms.ValidationError(u"请将行业名称缩减至8个字以下")
        return trade


class RegistBasisForm(forms.ModelForm):

    SEX_CHOICES = (
        ('w', _(u'女')),
        ('m', _(u'男')),
    )
    INDENTITY_CHOICES = (
        ('entrepreneurs', _(u'创业者')),
        ('investors ', _(u'投资人')),
        ('other', _(u'其他')),
    )
    name = forms.CharField(max_length=8, label=_(u'姓名'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={"id": "sex"}), choices=SEX_CHOICES, label=_(u'性别'))
    identity = forms.ChoiceField(widget=forms.RadioSelect(attrs={"id": "identity"}), choices=INDENTITY_CHOICES, label=_(u'身份'))
    company = forms.CharField(label=_(u'公司'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    job = forms.CharField(label=_(u'职位'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    email = forms.EmailField(label=_(u'邮箱'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    mobile_phone = forms.CharField(label=_(u'手机'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    trade = forms.CharField(label=_(u'行业'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    city = forms.CharField(label=_(u'城市'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    # wechat = forms.CharField(label=_(u'微信'), required=False, widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    openid = forms.CharField(label=_(u'微信id'), required=False)
    image = forms.URLField(label=_(u'微信头像'), required=False)

    class Meta:
        model = Member
        exclude = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_before = Member.objects.filter(email=email)
        if email_before:
            email_before = email_before[0].email
            if email == email_before:
                raise forms.ValidationError(_(u'您好，此邮箱地址已被注册'))
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if mobile_phone:
            def length(string):
                if not isinstance(string, unicode):
                    string = string.decode('utf-8')
                count = 0
                for c in string:
                    if u'\u0100' < c < u'\uffff':
                        count += 2
                    else:
                        count += 1
                return count
            try:
                int(mobile_phone)
            except:
                raise forms.ValidationError(_(u'请填写整数'))
            if length(mobile_phone) != 11:
                raise forms.ValidationError(_(u'请输入正确的手机号！'))
            if mobile_phone[0] != '1':
                raise forms.ValidationError(_(u'第一位必须为1！'))
            phone = Member.objects.filter(mobile_phone=mobile_phone)
            if phone:
                phone = phone[0]
                if phone.mobile_phone == mobile_phone:
                    raise forms.ValidationError(_(u'您好，此手机号码已被注册'))
            return mobile_phone
        else:
            return mobile_phone

    def clean(self):
        # form = super(RegistBasisForm, self).clean()
        form = self.cleaned_data
        keys = form.keys()
        for key in keys:
            if key == 'openid' or key == 'image' or key == 'wechat':
               pass
            else:
                if form[key].strip() == u'':
                    msg = u'请不要输入空格！'
                    self._errors[key] = self.error_class([msg])
        return form

    def clean_trade(self):
        data = self.cleaned_data
        trade = data.get('trade')
        if len(trade) > 8:
            raise forms.ValidationError(u"请将行业名称缩减至8个字以下")
        return trade

    # def clean_wechat(self):
    #     wechat = self.cleaned_data.get('wechat')
    #     if wechat == u'':
    #         raise forms.ValidationError(u"此项不能为空")
    #     return wechat


class MobileDateInput(forms.DateInput):
    input_type = 'date'


class RegistEducateForm(forms.ModelForm):
    school = forms.CharField(required=False, label=_(u'学校'))
    degree = forms.CharField(label=_(u'学位'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    department = forms.CharField(label=_(u'系别'), widget=forms.TextInput(attrs=dict(placeholder=u'必填')))
    enrol_date = forms.DateField(required=False, label=_(u'入学年月'),
                                 widget=MobileDateInput(attrs={'class': "date", 'placeholder': u"必填"}))
    graduate_date = forms.DateField(required=False, label=_(u'毕业年月'),
                                    widget=MobileDateInput(attrs={'class': "date", 'placeholder': u"必填"}))
    second_school = forms.CharField(required=False, label=_(u'学校'), widget=forms.TextInput(attrs=dict(placeholder=u'选填')))
    second_degree = forms.CharField(required=False, label=_(u'学位'), widget=forms.TextInput(attrs=dict(placeholder=u'选填')))
    second_department = forms.CharField(required=False, label=_(u'系别'), widget=forms.TextInput(attrs=dict(placeholder=u'选填')))
    second_enrol_date = forms.DateField(required=False, label=_(u'入学年月'),
                                        widget=MobileDateInput(attrs={'class': "date", 'placeholder': u"选填"}))
    second_graduate_date = forms.DateField(required=False, label=_(u'毕业年月'),
                                           widget=MobileDateInput(attrs={'class': "date", 'placeholder': u"选填"}))

    class Meta:
        model = Educate
        fields = ['school', 'degree', 'department', 'enrol_date', 'graduate_date',
                  'second_school', 'second_degree', 'second_department', 'second_enrol_date', 'second_graduate_date']

    def clean_department(self):
        data = self.cleaned_data
        department = data.get('department')
        if len(department) > 8:
            raise forms.ValidationError(u"请将系别名称缩减至8个字以下")
        return department

    def clean_enrol_date(self):
        import time
        now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data = self.cleaned_data
        enrol_date = data.get('enrol_date')
        if not enrol_date:
            raise forms.ValidationError(u'您好，入学年月和毕业年月是必填项！')
        if str(enrol_date) > str(now):
            raise forms.ValidationError(u"您好，入学年月不可超过当前时间")
        return enrol_date

    def clean_graduate_date(self):
        data = self.cleaned_data
        graduate_date = data.get('graduate_date')
        enrol_date = data.get('enrol_date')
        if not graduate_date:
            raise forms.ValidationError(u'您好，入学年月和毕业年月是必填项！')
        if graduate_date and enrol_date:
            if str(graduate_date) < str(enrol_date):
                raise forms.ValidationError(u"您好，毕业年月不可早于入学时间")
        return graduate_date

    def clean_second_enrol_date(self):
        import time
        now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data = self.cleaned_data
        second_enrol_date = data.get('second_enrol_date')
        if second_enrol_date:
            if str(second_enrol_date) > str(now):
                raise forms.ValidationError(u"您好，入学年月不可超过当前时间")
        return second_enrol_date

    def clean_second_graduate_date(self):
        data = self.cleaned_data
        second_enrol_date = data.get('second_enrol_date')
        second_graduate_date = data.get('second_graduate_date')
        if second_enrol_date and second_graduate_date:
            if str(second_graduate_date) < str(second_enrol_date):
                raise forms.ValidationError(u"您好，毕业年月不可早于入学时间")
        return second_graduate_date

    def clean(self):
        # form = super(RegistEducateForm, self).clean()
        form = self.cleaned_data
        keys = form.keys()
        for key in keys:
            if form[key] == None or key == 'second_school' or key == 'second_degree' or key == 'second_department':
                pass
            else:
                educate_key = form[key]
                if type(educate_key) == datetime.date:
                    educate_key = educate_key.strftime('%Y-%m-%d')
                if educate_key.strip() == u'':
                    msg = u'请不要输入空格！'
                    self._errors[key] = self.error_class([msg])
        return form


class RegistOccupationForm(forms.ModelForm):
    OCC_CHOICE = (
        ('full-time', _(u'已在全职创业')),
        ('part-time', _(u'已在兼职创业')),
        ('ready-full', _(u'准备全职创业')),
        ('ready-part', _(u'准备兼职创业')),
        ('MetPartner', _(u'以认识朋友为主'))
    )
    occupation_state = forms.ChoiceField(widget=forms.Select(), choices=OCC_CHOICE, label=_(u'创业状态'))
    item_brief = forms.CharField(required=False, widget=forms.Textarea(attrs=dict(placeholder=u'大体概述')), label=_(u'项目简介'))
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs=dict(placeholder=u'备注')), label=_(u'备注信息'))

    class Meta:
        model = Occupation
        fields = ['occupation_state', 'item_brief', 'remarks']


class RegistDemandForm(forms.ModelForm):
    demand = forms.CharField(required=False, widget=forms.Textarea(attrs=dict(placeholder=u'需求信息,例如：以认识的朋友为主')), label=_(u'需求资源'))
    supply = forms.CharField(required=False, widget=forms.Textarea(attrs=dict(placeholder=u'提供信息，例如：云计算领域技术合作')), label=_(u'提供资源'))

    class Meta:
        model = Demand
        fields = ['demand', 'supply']


IMPORT_FILE_TYPES = ['.xls', ]


class FileUploadForm(forms.Form):
    upload_xls = forms.FileField(label=u'文件')

    def clean_upload_xls(self):
        import os
        upload_xls = self.cleaned_data['upload_xls']
        extension = os.path.splitext(upload_xls.name )[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError(
                u'%s 不是一个有效的excel文件. '
                u'请确定你的文件格式. (不支持Excel 2007)' % extension )
        else:
            return upload_xls
