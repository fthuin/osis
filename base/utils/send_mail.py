# -*- coding: utf-8 -*-
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

"""
Utility files for mail sending
"""
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from backoffice.settings import DEFAULT_FROM_EMAIL


def send_mail_after_scores_submission(persons, learning_unit_name):
    """
    Send an email to all the teachers after the scores submission for a learning unit
    :param persons: The list of the teachers of the leaning unit
    :param learning_unit_name: The name of the learning unit for wihch scores were submitted
    """

    subject = _('Sumbmission of scores for {0}.').format(learning_unit_name)
    html_message = ''.join([
        str(_('<p>Hi, </p>')),
        str(_('<p>We inform you that a scores submission was made for {learning_unit_name}.</p></br>')).format(
            learning_unit_name=learning_unit_name),
        str(_('The OSIS Team<br>')),
        EMAIL_SIGNATURE,
    ])
    message = ''.join([
        str(_('Hi, \n')),
        str(_('We inform you that a scores submission was made for {learning_unit_name}.\n\n')).format(
            learning_unit_name=learning_unit_name),
        str(_('The OSIS Team.')),
    ])

    send_mail(subject=subject,message=message,recipient_list=[person.email for person in persons],html_message=html_message,from_email=DEFAULT_FROM_EMAIL)


def send_mail_after_academic_calendar_changes(academic_calendar, offer_year_calendar, programme_managers):
    """
    Send an email to all the programme manager after changes has been made on a offer_year_calendar with customized
    = True
    :param academic_calendar:
    :param offer_year_calendar:
    """

    subject = _('Watch out - Changes has been made on %s, academic calendar (%s)') % (offer_year_calendar.offer_year, academic_calendar)
    html_message = ''.join([
        str(_('<p>Hi, </p>')),
        str(_('<p>We inform you that changes has been made on \'{offer_year}\'({acronym}), academic calendar ({academic_calendar}).</p></br>')).format(
            offer_year=offer_year_calendar.offer_year.title,acronym=offer_year_calendar.offer_year.acronym, academic_calendar=academic_calendar),
        str(_('The OSIS Team<br>')),
        EMAIL_SIGNATURE,
    ])
    message = ''.join([
        str(_('Hi, \n')),
        str(_('We inform you that changes has been made on \'{offer_year}\'({acronym}), academic calendar ({academic_calendar}).\n\n')).format(
            offer_year=offer_year_calendar.offer_year.title,acronym=offer_year_calendar.offer_year.acronym, academic_calendar=academic_calendar),
        str(_('The OSIS Team.')),
    ])

    send_mail(subject=subject,message=message,recipient_list=[programme_manager.person.email for programme_manager in programme_managers],html_message=html_message,from_email='DEFAULT_FROM_EMAIL')


GENDER_TITLE_MAP={
    'M': _('Mister'),
    'F': _('Miss'),
    'U': ''
}

EMAIL_SIGNATURE = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1"><title>signature</title>
    </head>
    <body>
        <table cellpadding="5" cellspacing="5">
            <tbody>
                <tr>
                    <td width="60">
                        <img src="http://www.uclouvain.be/cps/ucl/doc/ac-arec/images/logo-signature.png">
                    </td>
                    <td>
                        <img src="https://osis.uclouvain.be/static/img/logo_osis.png">
                    </td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
"""
