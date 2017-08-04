# -*- coding: utf-8 -*-
import xlrd
from member.utils import iframe_jsonify
from regist.models import Member, Educate, Occupation, Demand
from datetime import date
import datetime

def deal_with_sheet(book, sheet, row):
        rowval = sheet.row_values(row)
        enrol_date = xlrd.xldate_as_tuple(rowval[9], book.datemode)
        enrol_date = date(*enrol_date[:3])
        member = Member.objects.create(
            name=rowval[2],
            sex=rowval[7],
            company=rowval[3],
            job=rowval[4],
            email=rowval[15],
            mobile_phone=int(rowval[16]),
            city=rowval[5],
            wechat=rowval[6],
        )
        Educate.objects.filter(member=member).update(
            degree=rowval[10],
            department=rowval[8],
            enrol_date=enrol_date,
        )
        Occupation.objects.filter(member=member).update(
            occupation_state=rowval[11],
            item_brief=rowval[12],
            remarks=rowval[17],
        )
        Demand.objects.filter(member=member).update(
            demand=rowval[13],
            supply=rowval[14],
        )
        if rowval[1]:
            create = xlrd.xldate_as_tuple(rowval[1], book.datemode)
            create = datetime.datetime(*create)
            id = member.id
            member = Member.objects.get(pk=id)
            member.create = create
            member.save()


def check_with_sheet(sheet):
    clos = sheet.col_values(0)
    clos = list(clos)
    clos.pop(0)
    if "" in clos:
        return iframe_jsonify(state=False, data=u"序号填写不全，请检查后重新上传！")
    if not clos:
        return iframe_jsonify(state=False, data=u"没有写入序号！")
    nrows = sheet.nrows
    for row in xrange(2, nrows):
        rowval = sheet.row_values(row)
        sex = rowval[7]
        state = rowval[11]
        mobile_phone = str(int(rowval[16]))
        email = rowval[15]
        phonesql = Member.objects.filter(mobile_phone=mobile_phone)
        emailsql = Member.objects.filter(email=email)
        try:
            enrol_date = xlrd.xldate_as_tuple(rowval[9], 1)
            enrol_date = date(*enrol_date[:3])
        except:
            enrol_date = None
        if len(rowval) < 18:
            return iframe_jsonify(state=False, data=u"表格内容缺少！")
        if "" in rowval:
            if "" in rowval[1]:
                pass
            else:
                return iframe_jsonify(state=False, data=u"内容不允许为空！")
        if sex not in (u'男', u'女'):
            return iframe_jsonify(state=False, data=u"性别请输入男或女！")
        if not enrol_date:
            return iframe_jsonify(state=False, data=u"请输入日期格式为: YYYY-MM-DD！")
        if phonesql:
            return iframe_jsonify(state=False, data=u"电话号码：%s已存在，请重新填写！" % mobile_phone)
        if emailsql:
            return iframe_jsonify(state=False, data=u"电子邮箱：%s已存在，请重新填写！" % email)
        if state not in (u'已在全职创业', u'已在兼职创业', u'准备兼职创业', u'准备全职创业', u'以认识朋友为主'):
            return iframe_jsonify(state=False, data=u"请输入正确的创业状态！")