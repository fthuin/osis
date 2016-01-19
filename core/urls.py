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
from django.conf.urls import url
from django.contrib.auth.views import login,logout_then_login

from . import views
from . import exportUtils
from . import uploadXlsUtils
from core.authentication import shibbollethUser

urlpatterns = [
    url(r'^$', views.home, name='home'),

    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', shibbollethUser.logout_with_delete_cookie, name='logout'),

    url(r'^studies/$', views.studies, name='studies'),
    url(r'^studies/assessements/$', views.assessements, name='assessements'),
    url(r'^studies/assessements/scores_encoding$', views.scores_encoding, name='scores_encoding'),
    url(r'^studies/assessements/scores_encoding/online/([0-9]+)/$', views.online_encoding, name='online_encoding'),
    url(r'^studies/assessements/scores_encoding/online/([0-9]+)/form$', views.online_encoding_form, name='online_encoding_form'),
    url(r'^studies/assessements/scores_encoding/all_notes_printing/([0-9]+)/$', views.all_notes_printing, name='all_notes_printing'),
    url(r'^studies/assessements/scores_encoding/notes_printing/([0-9]+)/([0-9]+)/$', views.notes_printing, name='notes_printing'),
    url(r'^studies/assessements/scores_encoding/online/([0-9]+)/$', views.online_encoding, name='online_encoding'),
    url(r'^studies/assessements/scores_encoding/xlsdownload/([0-9]+)/([0-9]+)/([0-9]+)/$',views.export_xls, name='scores_encoding_download'),
    url(r'^studies/assessements/scores_encoding/upload/([0-9]+)/([0-9]+)/([0-9]+)/$',uploadXlsUtils.upload_scores_file,name='upload_encoding'),
]
