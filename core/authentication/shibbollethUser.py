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
import subprocess
import urllib
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib import auth
from django.contrib.auth import backends, logout
from django.contrib.sessions.models import Session
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from pip._vendor.requests.packages import urllib3
from osis_backend import settings


class ShibbollethUserBackend(RemoteUserBackend):

    def authenticate(self, remote_user,user_info):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not remote_user:
            return
        user = None
        username = self.clean_username(remote_user)

        UserModel = backends.get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username
            })
            if created:
                user = self.configure_user(user,user_info)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass
        return user

    def clean_username(self, username):
        return username.split("@")[0]

    def configure_user(self, user,user_info):
        user.last_name = user_info['USER_LAST_NAME']
        user.first_name = user_info['USER_FIRST_NAME']
        user.email = user_info['USER_EMAIL']

        # TEST SHIBBOLLETH!!!! A suprimer !!!!!
        if(user.email == 'gaetan.lamarca@uclouvain.be') or (user.email == 'hildeberto.mendonca@uclouvain.be'):
            user.is_staff = True
            user.is_superuser = True

        user.save()





class ShibbollethUserMiddleware(RemoteUserMiddleware):
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                self._remove_invalid_user(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        userInfos = self.getShibbollethInfos(request)
        user = auth.authenticate(remote_user=username,user_info=userInfos)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def getShibbollethInfos(self,request):
        userFirstName = request.META['givenName']
        userLastName = request.META['sn']
        userEmail = request.META['mail']
        return {
            'USER_FIRST_NAME' : userFirstName,
            'USER_LAST_NAME' : userLastName,
            'USER_EMAIL' : userEmail,
            }


def logout_with_delete_cookie(request):
    user = request.user
    cookies = request.COOKIES
    logout(request)
    request.session.flush()
    response = HttpResponseRedirect(reverse('home'))
    for key in cookies.keys():
        print(''.join(['Key : ',key]))
        response.delete_cookie(key)
    #[s.delete() for s in Session.objects.all() if str(s.get_decoded().get('_auth_user_id')) == str(user.id)]
    urllib.request.urlopen(settings.LOGOUT_EXTRA)
    return response

