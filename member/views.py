# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import itertools
from django.utils import timezone
from django.utils.timezone import make_naive
from regist.models import Member, Educate, Occupation, Demand
from .forms import MemberFilter
from doodoll_kit.decorators import jsonify
from urllib import quote
from django.core.urlresolvers import reverse


class ExcelFileExportMixin(object):

    excel_file_name = "download"

    def get_excel_file_name(self):
        return self.excel_file_name
    def get_excel_headers(self, context):
        return context['headers']

    def get_excel_results(self, context):
        return context['results']

    def get_cells(self, context):
        headers = self.get_excel_headers(context)
        results = self.get_excel_results(context)

        for row, el in enumerate(itertools.chain([headers], results)):
            rowdata = el['row'] if 'row' in el else el
            for col, val in enumerate(rowdata):
                yield row, col, val

    def render_to_excel(self, context):
        import xlwt

        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('untitled')

        default_style = xlwt.Style.default_style
        datetime_style = xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm')
        date_style = xlwt.easyxf(num_format_str='yyyy-mm-dd')

        for row, col, val in self.get_cells(context):
            if isinstance(val, datetime.datetime):
                style = datetime_style
            elif isinstance(val, datetime.date):
                style = date_style
            else:
                style = default_style

            sheet.write(row, col, val, style=style)

        filename = self.get_excel_file_name()

        response = HttpResponse(mimetype='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % quote(filename.encode('utf-8'))
        book.save(response)

        return response


@login_required
def member_index(request):
    return redirect('member_list')


@login_required
def member_list(request):
    error = []
    members = Member.objects.all()
    sort = request.GET.get('sort', None)
    request.session['sort'] = sort
    if request.session.get('sort') == '-1':
        members = members.order_by('create')
    filter_set = MemberFilter(request.GET, queryset=members)
    members = filter_set.qs
    if not members:
        error = u'对不起，没有符合该搜索条件的用户，请重新搜索！'
    if request.GET.get('export') in ['1', 'true']:
        return MemberListExport(members).get_response()
    if request.GET.get('pre') == 'up':
        pgup = request.session.get('pgup')
        filter_set = MemberFilter(pgup, queryset=members)
        members = filter_set.qs
    request.session['pgup'] = request.GET

    return render(request, 'member_list.html', {
        'members': members,
        'form': filter_set.form,
        'error': error,
    })


@jsonify
@login_required
def member_details(request):
    id = request.GET.get('id', None)
    try:
        member = Member.objects.get(pk=int(id))
    except Exception, e:
        return dict(errors=str(e))
    educate = Educate.objects.filter(member=member)[0]
    occupation = Occupation.objects.filter(member=member)
    demand = Demand.objects.filter(member=member)

    if request.GET.get('export') in ['1', 'true']:
        members = Member.objects.filter(pk=int(id))
        return MemberListExport(members).get_response()
    if request.GET.get('pre') == 'del':
        member.delete()
        return redirect('member_list')

    return render(request, 'member_details.html', {
        'member': member,
        'educate': educate,
        'occupation': occupation,
        'demand': demand
    })


class MemberListExport(ExcelFileExportMixin):
    excel_file_name = u'会员资源展示表'

    def __init__(self, queryset):
        self.members = queryset

    def get_excel_headers(self, context):
        return [u'姓名', u'性别', u'身份', u'公司', u'职位', u'邮箱',
                u'手机', u'行业', u'城市', u'微信', u'第一学历信息', u'创业状态',
                u'是否对其他俱乐部校友可见', u'是否关注', u'审核状态', u'项目简介',
                u'备注', u'需求资源', u'提供资源', u'添加时间']

    def get_excel_results(self, context):

        def covert_dt(dt):
            if dt:
                dt = dt + timezone.timedelta(hours=8)
                return make_naive(dt, dt.tzinfo)

        for member in self.members:
            row = [
                member.name,
                member.get_sex_display(),
                member.get_identity_display(),
                member.company,
                member.job,
                member.email,
                member.mobile_phone,
                member.trade,
                member.city,
                member.wechat,
                member.get_first_educate,
                member.get_occupation_state,
                member.get_public,
                member.get_attention,
                member.get_examine,
                member.occupation.item_brief,
                member.occupation.remarks,
                member.demand.demand,
                member.demand.supply,
                covert_dt(member.create),
            ]
            yield row

    def get_response(self):
        return self.render_to_excel({})


@jsonify
@login_required
def member_attention(request):
    id = request.GET.get('id', None)
    attention = request.GET.get('attention', '0')
    try:
        member = Member.objects.get(pk=id)
    except:
        return dict(state=False, errors=str('不存在该会员'))
    demand = Demand.objects.get(member=member)
    demand.attention = attention
    demand.save()
    if attention == '0':
        data = dict(attention=1, attention_display=u"关注")
    if attention == '1':
        data = dict(attention=0, attention_display=u'已关注')
    return dict(state=True, data=data)


@jsonify
@login_required
def member_examine(request):
    id = request.GET.get('id', None)
    examine = request.GET.get('examine', '0')
    try:
        member = Member.objects.get(pk=id)
    except:
        return dict(state=False, errors=str('不存在该会员'))
    demand = Demand.objects.get(member=member)
    demand.examine = examine
    demand.save()
    return dict(state=True, data=str(demand.examine))


@login_required
def member_upload_excel(request):
    from regist.forms import FileUploadForm
    from member.utils import iframe_jsonify, errors_to_json
    from member.tasks import check_with_sheet, deal_with_sheet
    import xlrd
    if request.method == "POST":
        form = FileUploadForm(request.POST, files=request.FILES)
        if form.is_valid():
            xls = form.cleaned_data['upload_xls']
            book = xlrd.open_workbook(file_contents=xls.read())
            try:
                sheet = book.sheet_by_name(u'Sheet1')
            except:
                return iframe_jsonify(state=False, data=u"工作表名字需为'Sheet1'！")
            nrows = sheet.nrows
            msg = check_with_sheet(sheet)
            if msg:
                return msg
            for row in xrange(1, nrows):
                deal_with_sheet(book, sheet, row)
            return iframe_jsonify(state=True, reverse_url=reverse('member_list'))
        else:
            return iframe_jsonify(state=False, error=errors_to_json(form.errors))