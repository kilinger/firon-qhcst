#-*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Member(models.Model):

    SEX_CHOICES = (
        ('w', _(u'女')),
        ('m', _(u'男')),
    )
    INDENTITY_CHOICES = (
        ('entrepreneurs', _(u'创业者')),
        ('investors ', _(u'投资人')),
        ('other', _(u'其他')),
    )
    name = models.CharField(max_length=30, verbose_name=_(u'姓名'))
    sex = models.CharField(max_length=2, choices=SEX_CHOICES,  verbose_name=_(u'性别'))
    identity = models.CharField(max_length=13,  choices=INDENTITY_CHOICES, verbose_name=_(u'身份'))
    company = models.CharField(max_length=50, verbose_name=_(u'公司'))
    job = models.CharField(max_length=10, verbose_name=_(u'职位'))
    email = models.EmailField(verbose_name=_(u'邮箱'))
    mobile_phone = models.CharField(max_length=30, verbose_name=_(u'手机'))
    trade = models.CharField(max_length=30, verbose_name=_(u'行业'))
    city = models.CharField(max_length=30, verbose_name=_(u'城市'))
    wechat = models.CharField(max_length=20, blank=True, verbose_name=_(u'微信'))
    openid = models.CharField(max_length=255, blank=True, default='', verbose_name=_(u'微信id'))
    image = models.URLField(blank=True, default='', verbose_name=_(u'微信头像'))
    create = models.DateTimeField(auto_now_add=True, verbose_name=_(u'创建时间'))

    class Meta:
        verbose_name = u'会员'
        verbose_name_plural = u'会员'
        ordering = ('-create', )

    def __str__(self):
        return self.name

    @property
    def get_attention(self):
        if hasattr(self, 'demand'):
            return self.demand.get_attention_display()
        return

    @property
    def get_examine(self):
        if hasattr(self, 'demand'):
            return self.demand.get_examine_display()
        return

    @property
    def get_public(self):
        if hasattr(self, 'occupation'):
            return self.occupation.get_public_display()
        return

    @property
    def get_occupation_state(self):
        if hasattr(self, 'occupation'):
            return self.occupation.get_occupation_state_display()
        return

    @property
    def get_first_educate(self):
        if hasattr(self, 'educate'):
            educate_info = list([self.educate.school, self.educate.degree, self.educate.department])
            return "/".join(educate_info)

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return


def create_member_profile(sender, instance, created, **kwargs):
        if created:
            educate, created_educate = Educate.objects.get_or_create(member=instance)
            occupation, created_occupation = Occupation.objects.get_or_create(member=instance)
            demand, created_demand = Demand.objects.get_or_create(member=instance)

post_save.connect(create_member_profile, sender=Member)


@python_2_unicode_compatible
class Educate(models.Model):
    member = models.OneToOneField('Member')
    school = models.CharField(max_length=30, default=u'清华大学', verbose_name=_(u'学校'))
    degree = models.CharField(max_length=30, verbose_name=_(u'学位'))
    department = models.CharField(max_length=30, verbose_name=_(u'系别'))
    enrol_date = models.DateField(blank=True, null=True, verbose_name=_(u'入学年月'))
    graduate_date = models.DateField(blank=True, null=True, verbose_name=_(u'毕业年月'))
    second_school = models.CharField(blank=True, max_length=30, default=u'清华大学', verbose_name=_(u'学校'))
    second_degree = models.CharField(blank=True, max_length=30, verbose_name=_(u'学位'))
    second_department = models.CharField(blank=True, max_length=30, verbose_name=_(u'系别'))
    second_enrol_date = models.DateField(blank=True, null=True, verbose_name=_(u'入学年月'))
    second_graduate_date = models.DateField(blank=True, null=True, verbose_name=_(u'毕业年月'))

    class Meta:
        verbose_name = u'教育'
        verbose_name_plural = u'教育'

    def __str__(self):
        return self.school


@python_2_unicode_compatible
class Occupation(models.Model):
    OCC_CHOICE = (
        ('full-time', _(u'已在全职创业')),
        ('part-time', _(u'已在兼职创业')),
        ('ready-full', _(u'准备全职创业')),
        ('ready-part', _(u'准备兼职创业')),
        ('MetPartner', _(u'以认识朋友为主'))
    )
    PUBLIC_CHOICES = (
        ('1', u'全部可见'),
        ('0', u'隐藏联系方式')
    )
    member = models.OneToOneField('Member', unique=True)
    occupation_state = models.CharField(max_length=10,
                                        choices=OCC_CHOICE,
                                        default='full-time',
                                        verbose_name=_(u'创业状态'))
    public = models.CharField(max_length=2, choices=PUBLIC_CHOICES, default='0', verbose_name=_(u'是否对其他俱乐部校友可见'))
    item_brief = models.TextField(blank=True, max_length=500, verbose_name=_(u'项目简介'))
    remarks = models.TextField(blank=True, max_length=200, verbose_name=_(u'备注信息'))

    class Meta:
        verbose_name = u'创业状况'
        verbose_name_plural = u'创业状况'

    def __str__(self):
        return self.occupation_state


@python_2_unicode_compatible
class Demand(models.Model):
    ATT_CHOICES = (
        ('0', u'未关注'),
        ('1', u'关注')
    )
    EXAMINE_CHOICES = (
        ('0', u'待审核'),
        ('1', u'审核通过'),
        ('2', u'已拒绝')
    )
    member = models.OneToOneField('Member', unique=True)
    demand = models.TextField(blank=True, max_length=200, verbose_name=_(u'需求资源'))
    supply = models.TextField(blank=True, max_length=200, verbose_name=_(u'提供资源'))
    examine = models.CharField(max_length=2, default='0', choices=EXAMINE_CHOICES, verbose_name=_(u'审核状态'))
    attention = models.CharField(max_length=1, choices=ATT_CHOICES, default='0', verbose_name=_(u'关注状态'))

    class Meta:
        verbose_name = u"资源"
        verbose_name_plural = u"资源"

    def __str__(self):
        return self.demand
