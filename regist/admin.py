# -*- coding: utf-8 -*-
from django.contrib import admin
from regist.models import Member, Educate, Occupation, Demand


class MemberAdmin(admin.ModelAdmin):

    search_fields = ('name', 'email')
    list_display = ('name', 'email')


class EducateAdmin(admin.ModelAdmin):
    search_fields = ('member__name', )
    list_display = ('member__name', 'school', 'degree', 'department',)

    def member__name(self, obj):
        return obj.member.name


class OccupationAdmin(admin.ModelAdmin):
    search_fields = ('member__name', )
    list_display = ('member__name', 'occupation_state', 'public',)

    def member__name(self, obj):
        return obj.member.name


class DemandAdmin(admin.ModelAdmin):
    search_fields = ('member__name', )
    list_display = ('member__name', 'examine', 'attention')

    def member__name(self, obj):
        return obj.member.name


admin.site.register(Member, MemberAdmin)
admin.site.register(Educate, EducateAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Demand, DemandAdmin)