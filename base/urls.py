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
from django.contrib.auth.views import login, logout

from base.utils import upload_xls_utils
from base.views import learning_unit, offer, common, score_encoding, institution, academic_calendar

#app_name = 'base'

urlpatterns = [
    url(r'^$', common.home, name='home'),

    # Please, organize the urls in alphabetic order.

    url(r'^catalog/$', common.catalog, name='catalog'),

    url(r'^institution/$', institution.institution, name='institution'),

    url(r'^learning_units/$', learning_unit.learning_units, name='learning_units'),
    url(r'^learning_units/search$', learning_unit.learning_units_search, name='learning_units_search'),
    url(r'^learning_units/([0-9]+)/$', learning_unit.learning_unit_read, name='learning_unit_read'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^offers/$', offer.offers, name='offers'),
    url(r'^offers/search$', offer.offers_search, name='offers_search'),
    url(r'^offers/([0-9]+)/$', offer.offer_read, name='offer_read'),

    url(r'^studies/$', common.studies, name='studies'),
    url(r'^studies/assessments/$', common.assessments, name='assessments'),
    url(r'^studies/assessments/scores_encoding$', score_encoding.scores_encoding, name='scores_encoding'),
    url(r'^studies/assessments/scores_encoding/online/([0-9]+)/$', score_encoding.online_encoding, name='online_encoding'),
    url(r'^studies/assessments/scores_encoding/online/([0-9]+)/form$', score_encoding.online_encoding_form, name='online_encoding_form'),
    url(r'^studies/assessments/scores_encoding/online/([0-9]+)/submission$', score_encoding.online_encoding_submission, name='online_encoding_submission'),
    url(r'^studies/assessments/scores_encoding/online/([0-9]+)/double_form$', score_encoding.online_double_encoding_form, name='online_double_encoding_form'),
    url(r'^studies/assessments/scores_encoding/online/([0-9]+)/double_validation$', score_encoding.online_double_encoding_validation, name='online_double_encoding_validation'),
    url(r'^studies/assessments/scores_encoding/notes_printing_all/([0-9]+)/$', score_encoding.notes_printing_all, name='notes_printing_all'),
    url(r'^studies/assessments/scores_encoding/notes_printing/([0-9]+)/([0-9]+)/$', score_encoding.notes_printing, name='notes_printing'),
    url(r'^studies/assessments/scores_encoding/xlsdownload/([0-9]+)/([0-9]+)/([0-9]+)/$',score_encoding.export_xls, name='scores_encoding_download'),
    url(r'^studies/assessments/scores_encoding/upload/([0-9]+)/([0-9]+)/([0-9]+)/$', upload_xls_utils.upload_scores_file,name='upload_encoding'),

    url(r'^structures/$', institution.structures, name='structures'),
    url(r'^structures/search$', institution.structures_search, name='structures_search'),
    url(r'^structures/([0-9]+)/$', institution.structure_read, name='structure_read'),

    url(r'^academic_calendars/$', academic_calendar.academic_calendars, name='academic_calendars'),
    url(r'^academic_calendars/search$', academic_calendar.academic_calendars_search, name='academic_calendars_search'),
    url(r'^academic_calendars/([0-9]+)/$', academic_calendar.academic_calendar_read, name='academic_calendar_read'),

    ]