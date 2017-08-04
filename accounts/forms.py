#-*- coding: utf-8 -*-
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原始密码",
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is  None:
                raise forms.ValidationError(u"用户名和密码是不正确的.")
            elif not self.user.is_active:
                raise forms.ValidationError(u'账户已禁止登录')
        return self.cleaned_data

    def get_user(self):
        return self.user


class FindPwdForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        cd = self.cleaned_data
        email = cd.get('email')
        is_exist = User.objects.filter(email=email).exists()
        if not is_exist:
            raise forms.ValidationError(u"没有此用户")
        return email


class ResetPwdForm(forms.Form):
    new = forms.CharField(widget=forms.PasswordInput())
    sure = forms.CharField(widget=forms.PasswordInput())

    def clean_new(self):
        cd = self.cleaned_data
        new = cd.get('new')

        if len(new) < 6:
            raise forms.ValidationError(u"请输入一个不小于6位的密码！")
        return new

    def clean_sure(self):
        cd = self.cleaned_data
        new = cd.get('new')
        sure = cd.get('sure')

        if new != sure:
            raise forms.ValidationError(u'密码不一致！')

        return sure