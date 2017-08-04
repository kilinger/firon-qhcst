#-*- coding: utf-8 -*-
from django import forms
import django_filters
from regist.models import Member


class MemberFilter(django_filters.FilterSet):
    SEX_CHOICES = (
        ('', u'不限'),
        ('w', u'女'),
        ('m', u'男'),
    )
    INDENTITY_CHOICES = (
        ('', u'不限'),
        ('entrepreneurs', u'创业者'),
        ('investors ', u'投资人'),
        ('other', u'其他'),
    )
    EXAMINE_CHOICES = (
        ('', u'不限'),
        ('0', u'待审核'),
        ('1', u'审核通过'),
        ('2', u'已拒绝')
    )
    ATT_CHOICES = (
        ('', u'不限'),
        ('0', u'未关注'),
        ('1', u'关注')
    )
    name = django_filters.CharFilter(name='name', lookup_type="icontains")
    city = django_filters.CharFilter(name='city', lookup_type="icontains")
    trade = django_filters.CharFilter(name='trade', lookup_type="icontains")
    sex = django_filters.ChoiceFilter(name='sex', choices=SEX_CHOICES, widget=forms.Select())
    identity = django_filters.ChoiceFilter(name='identity',
                                           choices=INDENTITY_CHOICES,
                                           widget=forms.Select())
    examine = django_filters.ChoiceFilter(name='demand__examine',
                                          choices=EXAMINE_CHOICES,
                                          widget=forms.Select())
    attention = django_filters.ChoiceFilter(name='demand__attention',
                                            choices=ATT_CHOICES,
                                            widget=forms.Select())

    class Meta:
        model = Member
        fields = ['name', 'city', 'trade', 'sex', 'identity', 'examine']