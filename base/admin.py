##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.contrib import admin

from .models import *

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'changed')
    fieldsets = ((None, {'fields': ('year',)}),)

admin.site.register(AcademicYear, AcademicYearAdmin)

class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'title', 'academic_year', 'start_date', 'end_date', 'changed')
    fieldsets = ((None, {'fields': ('academic_year', 'event_type', 'title', 'description', 'start_date', 'end_date')}),)

admin.site.register(AcademicCalendar, AcademicCalendarAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('acronym','title', 'changed')
    fieldsets = ((None, {'fields': ('acronym','title')}),)

admin.site.register(Offer, OfferAdmin)

class OfferYearAdmin(admin.ModelAdmin):
    list_display = ('offer','parent', 'title','academic_year', 'changed')
    fieldsets = ((None, {'fields': ('offer','academic_year','structure','acronym','title','parent')}),)

admin.site.register(OfferYear, OfferYearAdmin)

class OfferYearCalendarAdmin(admin.ModelAdmin):
    list_display = ('academic_calendar', 'offer_year', 'event_type', 'start_date', 'end_date', 'changed')
    list_filter = ('event_type',)
    fieldsets = ((None, {'fields': ('offer_year','academic_calendar','event_type','start_date','end_date')}),)

admin.site.register(OfferYearCalendar, OfferYearCalendarAdmin)

class OfferEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('offer_year','student', 'date_enrollment', 'changed')
    fieldsets = ((None, {'fields': ('offer_year','student','date_enrollment')}),)

admin.site.register(OfferEnrollment, OfferEnrollmentAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name' , 'middle_name', 'last_name', 'username','email', 'gender','global_id', 'national_id', 'changed')
    search_fields = ['first_name', 'middle_name', 'last_name', 'user__username','email']
    fieldsets = ((None, {'fields': ('user','global_id','national_id','gender','first_name','middle_name','last_name','email')}),)

admin.site.register(Person, PersonAdmin)

class LearningUnitAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'title', 'start_year', 'end_year', 'changed')
    fieldsets = ((None, {'fields': ('acronym','title','description','start_year','end_year')}),)

admin.site.register(LearningUnit, LearningUnitAdmin)

class LearningUnitYearAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'title', 'academic_year', 'credits', 'changed')
    fieldsets = ((None, {'fields': ('learning_unit','academic_year','acronym','title','credits','decimal_scores')}),)

admin.site.register(LearningUnitYear, LearningUnitYearAdmin)

class LearningUnitEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'learning_unit_year', 'date_enrollment', 'changed')
    fieldsets = ((None, {'fields': ('offer_enrollment','learning_unit_year','date_enrollment')}),)

admin.site.register(LearningUnitEnrollment, LearningUnitEnrollmentAdmin)

class SessionExamAdmin(admin.ModelAdmin):
    list_display = ('learning_unit_year', 'number_session', 'status', 'changed')
    list_filter = ('status',)
    fieldsets = ((None, {'fields': ('learning_unit_year','number_session','status','offer_year_calendar')}),)

admin.site.register(SessionExam, SessionExamAdmin)

class ExamEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'session_exam', 'score_final', 'justification_final', 'encoding_status', 'changed')
    list_filter = ('encoding_status',)
    fieldsets = ((None, {'fields': ('session_exam','learning_unit_enrollment')}),)

admin.site.register(ExamEnrollment, ExamEnrollmentAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'changed')
    fieldsets = ((None, {'fields': ('name', 'acronym')}),)

admin.site.register(Organization, OrganizationAdmin)

class StructureAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'title', 'part_of', 'changed')
    fieldsets = ((None, {'fields': ('acronym','title','part_of','organization')}),)

admin.site.register(Structure, StructureAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'registration_id', 'changed')
    fieldsets = ((None, {'fields': ('registration_id', 'person')}),)

admin.site.register(Student, StudentAdmin)

class TutorAdmin(admin.ModelAdmin):
    list_display = ('person', 'changed')
    fieldsets = ((None, {'fields': ('person',)}),)

admin.site.register(Tutor, TutorAdmin)

class ProgrammeManagerAdmin(admin.ModelAdmin):
    list_display = ('person', 'faculty')

admin.site.register(ProgrammeManager, ProgrammeManagerAdmin)

class AttributionAdmin(admin.ModelAdmin):
    list_display = ('tutor','function','learning_unit','start_date', 'end_date', 'changed')
    list_filter = ('function',)
    fieldsets = ((None, {'fields': ('learning_unit','tutor','function','start_date','end_date')}),)

admin.site.register(Attribution, AttributionAdmin)