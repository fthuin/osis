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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def internships_home(request):
    return render(request, "internships_home.html", {'section': 'internship'})

def internships_places(request):
    return render(request, "places.html", {'section': 'internship'})

def internships_students(request):
    return render(request, "students.html", {'section': 'internship'})

def internships(request):
    return render(request, "internships.html", {'section': 'internship'})

def internships_periods(request):
    return render(request, "periods.html", {'section': 'internship'})

def interships_masters(request):
    return render(request, "interships_masters.html", {'section': 'internship'})
