# -*- coding: utf-8 -*-
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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core import serializers
from base.forms import PersonUpdateForm
from base import models as mdl
from django.utils.translation import ugettext_lazy as _


def page_not_found(request):
    return render(request, 'page_not_found.html')


def access_denied(request):
    return render(request, 'access_denied.html')


def home(request):
    academic_yr = mdl.academic_year.current_academic_year()
    calendar_events = None
    if academic_yr:
        calendar_events = mdl.academic_calendar.find_academic_calendar_by_academic_year_with_dates(academic_yr.id)
    return render(request, "home.html", {'academic_calendar': calendar_events,
                                         'highlights': mdl.academic_calendar.find_highlight_academic_calendars()})


@login_required
def studies(request):
    return render(request, "studies.html", {'section': 'studies'})


@login_required
def assessments(request):
    return render(request, "assessments.html", {'section': 'assessments'})


@login_required
def catalog(request):
    return render(request, "catalog.html", {'section': 'catalog'})


@login_required
def academic_year(request):
    return render(request, "academic_year.html", {'section': 'academic_year'})


@login_required
def profile(request):
    person = mdl.person.find_person_by_user(request.user)
    if request.method == 'POST':
        form = PersonUpdateForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            if person:
                person.language = language
                person.save()
            else:
                person = mdl.person.Person(user=request.user, language=language)
                person = person.save()
            messages.success(request, _('Account details successfully updated!'))
    person = mdl.person.find_person_by_user(request.user)
    form = PersonUpdateForm(instance=person)
    fields = []
    if person:
        for field in mdl.person.Person._meta.get_fields():
            field_split = str(field).split('.')
            field = field_split[len(field_split) - 1]
            try:
                fields.append((field, getattr(person, str(field))))
            except AttributeError:
                print(str(field))
                pass
    return render(request, "profile.html", {'form':form,
                                            'person': person,
                                            'fields': fields})
