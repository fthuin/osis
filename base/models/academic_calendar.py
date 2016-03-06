# coding: utf8
##############################################################################
#
# OSIS stands for Open Student Information System. It's an application
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
from django.db import models
from django.utils import timezone
from django.contrib import admin
from base.models import academic_year
#from base.utils import send_mail

EVENT_TYPE = (
    ('ACADEMIC_YEAR', 'Academic Year'),
    ('DISSERTATIONS_SUBMISSION_SESS_1', 'Submission of academic dissertations - exam session 1'),
    ('DISSERTATIONS_SUBMISSION_SESS_2', 'Submission of academic dissertations - exam session 2'),
    ('DISSERTATIONS_SUBMISSION_SESS_3', 'Submission of academic dissertations - exam session 3'),
    ('EXAM_SCORES_SUBMISSION_SESS_1', 'Submission of exam scores - exam session 1'),
    ('EXAM_SCORES_SUBMISSION_SESS_2', 'Submission of exam scores - exam session 2'),
    ('EXAM_SCORES_SUBMISSION_SESS_3', 'Submission of exam scores - exam session 3'),
    ('DELIBERATIONS_SESS_1', 'Deliberations - exam session 1'),
    ('DELIBERATIONS_SESS_2', 'Deliberations - exam session 2'),
    ('DELIBERATIONS_SESS_3', 'Deliberations - exam session 3'),
    ('EXAM_SCORES_DIFFUSION_SESS_1', 'Diffusion of exam scores - exam session 1'),
    ('EXAM_SCORES_DIFFUSION_SESS_2', 'Diffusion of exam scores - exam session 2'),
    ('EXAM_SCORES_DIFFUSION_SESS_3', 'Diffusion of exam scores - exam session 3'),
    ('EXAM_ENROLLMENTS_SESS_1', 'Exam enrollments - exam session 1'),
    ('EXAM_ENROLLMENTS_SESS_2', 'Exam enrollments - exam session 2'),
    ('EXAM_ENROLLMENTS_SESS_3', 'Exam enrollments - exam session 3'))

class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'academic_year', 'start_date', 'end_date', 'changed')
    fieldsets = ((None, {'fields': ('academic_year', 'title', 'description', 'start_date', 'end_date')}),)


class AcademicCalendar(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed = models.DateTimeField(null=True)
    academic_year = models.ForeignKey(academic_year.AcademicYear)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    highlight_title = models.CharField(max_length=255, blank=True, null=True)
    highlight_description = models.CharField(max_length=255, blank=True, null=True)
    highlight_shortcut = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return u"%s %s" % (self.academic_year, self.title)

    # FIXME: This method was imported from models.py, I don't know if it is
    # still useful. @fthuin
    # def save(self,  *args, **kwargs):
    #     new = False
    #     start_date_before_change = None
    #     end_date_before_change = None
    #     if self.id is None:
    #         new = True
    #     else:
    #         academic_calendar = AcademicCalendar.objects.get(pk=self.id)
    #         start_date_before_change = academic_calendar.start_date
    #         end_date_before_change = academic_calendar.end_date
    #
    #     academic_calendar=super(AcademicCalendar, self).save(*args, **kwargs)
    #     academic_year = self.academic_year
    #
    #     if new:
    #         offer_year_list = OfferYear.find_offer_years_by_academic_year(academic_year.id)
    #         for offer_year in offer_year_list:
    #             offer_year_calendar=OfferYearCalendar()
    #             offer_year_calendar.academic_calendar = self
    #             offer_year_calendar.offer_year=offer_year
    #             offer_year_calendar.start_date = self.start_date
    #             offer_year_calendar.end_date = self.end_date
    #             offer_year_calendar.save()
    #     else:
    #         if (start_date_before_change is None and end_date_before_change is None ) or ((not start_date_before_change is None and start_date_before_change.strftime( '%d/%m/%Y')) != (not self.start_date is None and self.start_date.strftime( '%d/%m/%Y')) or (not end_date_before_change is None and end_date_before_change.strftime('%d/%m/%Y') != (not self.end_date is None and self.end_date.strftime( '%d/%m/%Y')))) :
    #             #Do this only if start_date or end_date changed
    #             offer_year_calendar_list = OfferYearCalendar.find_offer_years_by_academic_calendar(self)
    #             for offer_year_calendar in offer_year_calendar_list:
    #                 if offer_year_calendar.customized == True:
    #                     #an email must be sent to the programme manager
    #                     programme_managers = ProgrammeManager.objects.filter(faculty=offer_year_calendar.offer_year.structure)
    #                     if programme_managers and len(programme_managers) > 0:
    #                         send_mail.send_mail_after_academic_calendar_changes(self,offer_year_calendar, programme_managers)
    #                 else:
    #                     offer_year_calendar.start_date = self.start_date
    #                     offer_year_calendar.end_date = self.end_date
    #                     offer_year_calendar.save()
    #
    #     return academic_calendar

def current_academic_year():
    now = timezone.now()
    academic_calendar = AcademicCalendar.objects.filter(event_type='ACADEMIC_YEAR')\
                                                .filter(start_date__lte=now)\
                                                .filter(end_date__gte=now).first()
    if academic_calendar:
        return academic_calendar.academic_year
    else:
        return None

def find_by_id(academic_year_id):
    return AcademicCalendar.objects.get(pk=academic_year_id)

def find_highlight_academic_calendars():
    return AcademicCalendar.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now(),
                                           highlight_title__isnull=False, highlight_description__isnull=False,
                                           highlight_shortcut__isnull=False)


def find_academic_calendar_by_academic_year(academic_year_id):
    return AcademicCalendar.objects.filter(academic_year=academic_year_id).order_by('title')

def find_academic_calendar_by_event_type(academic_year_id, session_number):
    event_type_criteria = "EXAM_SCORES_SUBMISSION_SESS_"+str(session_number)
    return AcademicCalendar.objects.get(academic_year=academic_year_id, event_type=event_type_criteria)

def find_academic_calendar_by_academic_year_with_dates(academic_year_id):
    now = timezone.now()
    return AcademicCalendar.objects.filter(academic_year=academic_year_id,
                                           start_date__isnull=False,
                                           end_date__isnull=False) \
                                   .filter(models.Q(start_date__lte=now, end_date__gte=now) |
                                           models.Q(start_date__gte=now, end_date__gte=now)) \
                                   .order_by('start_date')


def find_academic_calendar_by_id(academic_calendar_id):
    return AcademicCalendar.objects.get(pk=academic_calendar_id)
