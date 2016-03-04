# coding: utf8
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
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from base.utils import send_mail
from datetime import datetime


class Person(models.Model):
    GENDER_CHOICES = (
        ('F',_('Female')),
        ('M',_('Male')),
        ('U',_('Unknown')))

    LANGUAGES_CHOICES = (
        ('FR',_('Français')),
        ('EN',_('English')))

    external_id  = models.CharField(max_length=100, blank=True, null=True)
    changed      = models.DateTimeField(null=True)
    user         = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    global_id    = models.CharField(max_length=10, blank=True, null=True)
    gender       = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES, default='U')
    national_id  = models.CharField(max_length=25, blank=True, null=True)
    first_name   = models.CharField(max_length=50, blank=True, null=True)
    middle_name  = models.CharField(max_length=50, blank=True, null=True)
    last_name    = models.CharField(max_length=50, blank=True, null=True)
    email        = models.EmailField(max_length=255, blank=True, null=True)
    phone        = models.CharField(max_length=30, blank=True, null=True)
    phone_mobile = models.CharField(max_length=30, blank=True, null=True)
    language     = models.CharField(max_length=30, null=True, choices=LANGUAGES_CHOICES, default='FR')

    def username(self):
        if self.user is None:
            return None
        return self.user.username

    @staticmethod
    def find_person(person_id):
        return Person.objects.get(id=person_id)

    @staticmethod
    def find_person_by_user(user):
        return Person.objects.get(user=user)

    def __str__(self):
        first_name = ""
        middle_name = ""
        last_name = ""
        if self.first_name :
            first_name = self.first_name
        if self.middle_name :
            middle_name = self.middle_name
        if self.last_name :
            last_name = self.last_name + ","

        return u"%s %s %s" % (last_name.upper(), first_name, middle_name)


class PersonAddress(models.Model):
    person      = models.ForeignKey(Person)
    label       = models.CharField(max_length=20)
    location    = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city        = models.CharField(max_length=255)
    country     = models.CharField(max_length=255)


class Tutor(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed     = models.DateTimeField(null=True)
    person      = models.ForeignKey(Person)

    @staticmethod
    def find_by_user(user):
        try:
            person = Person.find_person_by_user(user)
            # tutor = Tutor.objects.filter(person=person)
            tutor = Tutor.objects.get(person = person)

            return tutor
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return u"%s" % self.person


class Student(models.Model):
    external_id     = models.CharField(max_length=100, blank=True, null=True)
    changed         = models.DateTimeField(null=True)
    registration_id = models.CharField(max_length=10)
    person          = models.ForeignKey(Person)

    def __str__(self):
        return u"%s (%s)" % (self.person, self.registration_id)


class Organization(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed     = models.DateTimeField(null=True)
    name        = models.CharField(max_length=255)
    acronym     = models.CharField(max_length=15)
    website     = models.URLField(max_length=255, blank=True, null=True)
    reference   = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def find_by_id(id):
        return Organization.objects.get(pk=id)

    @staticmethod
    def find_by_acronym(acronym):
        return Organization.objects.filter(acronym__icontains=acronym)

    @staticmethod
    def find_by_name(name):
        return Organization.objects.filter(name__icontains=name)

    @staticmethod
    def find_by_acronym_name(acronym,name):
        return Organization.objects.filter(acronym__icontains=acronym,name__icontains=name)

    @staticmethod
    def find_all():
        return Organization.objects.all().order_by('acronym')

    def address(self):
        return OrganizationAddress.find_by_organization(self)

    def find_structure(self):
        return Structure.find_by_organization(self)

    def find_structure_tree(self):
        return Structure.find_tree_by_organization(self)


class OrganizationAddress(models.Model):
    organization = models.ForeignKey(Organization)
    label        = models.CharField(max_length=20, blank=True, null=True)
    location     = models.CharField(max_length=255, blank=True, null=True)
    postal_code  = models.CharField(max_length=20, blank=True, null=True)
    city         = models.CharField(max_length=255, blank=True, null=True)
    country      = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def find_by_organization(organization):
        organization_address_list =  OrganizationAddress.objects.filter(organization=organization)
        for organization_address in organization_address_list:
            #Supposed there is only one address for on organization
            return organization_address
        return None


class Structure(models.Model):
    external_id  = models.CharField(max_length=100, blank=True, null=True)
    changed      = models.DateTimeField(null=True)
    acronym      = models.CharField(max_length=15)
    title        = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, null=True)
    part_of      = models.ForeignKey('self', null=True, blank=True)

    def children(self):
        return Structure.objects.filter(part_of=self.pk)

    def serializable_object(self):
        obj = {'name': self.acronym, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

    @staticmethod
    def find_structures():
        return Structure.objects.all().order_by('acronym')

    @staticmethod
    def find_by_id(id):
        return Structure.objects.get(pk=id)

    def find_children(self):
        return Structure.objects.filter(part_of=self).order_by('acronym')

    def find_offer_years_by_academic_year(self):
        return OfferYear.objects.filter(structure=self).order_by('academic_year','acronym')

    @staticmethod
    def find_by_organization(organization):
        return Structure.objects.filter(organization=organization, part_of__isnull=True)

    @staticmethod
    def find_tree_by_organization(organization):
        structure= Structure.objects.filter(organization=organization)
        tags = []
        if not structure is None:
            for t in Structure.objects.filter(part_of=structure):
                tags.append(t.serializable_object())
        return tags

    def find_tree_by_structure(self):
        structure= Structure.objects.get(pk=self.id)
        tags = []
        if not structure is None:
            for t in Structure.objects.filter(part_of=structure):
                tags.append(t.serializable_object())
        return tags

    @staticmethod
    def find_by_acronym(acronym):
        return Structure.objects.get(acronym=acronym.strip())

    def __str__(self):
        return u"%s - %s" % (self.acronym, self.title)


class AcademicYear(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed     = models.DateTimeField(null=True)
    year        = models.IntegerField()

    @staticmethod
    def find_academic_year(id):
        return AcademicYear.objects.get(pk=id)

    @staticmethod
    def find_academic_years():
        return AcademicYear.objects.all().order_by('year')

    def __str__(self):
        return u"%s-%s" % (self.year, self.year + 1)


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


class AcademicCalendar(models.Model):
    external_id           = models.CharField(max_length=100, blank=True, null=True)
    changed               = models.DateTimeField(null=True)
    academic_year         = models.ForeignKey(AcademicYear)
    event_type            = models.CharField(max_length=50, choices=EVENT_TYPE)
    title                 = models.CharField(max_length=50, blank=True, null=True)
    description           = models.TextField(blank=True, null=True)
    start_date            = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date              = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    highlight_title       = models.CharField(max_length=255, blank=True, null=True)
    highlight_description = models.CharField(max_length=255, blank=True, null=True)
    highlight_shortcut    = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def current_academic_year():
        now = timezone.now()
        academic_calendar = AcademicCalendar.objects.filter(event_type='ACADEMIC_YEAR')\
                                                    .filter(start_date__lte=now)\
                                                    .filter(end_date__gte=now).first()
        if academic_calendar:
            return academic_calendar.academic_year
        else:
            return None

    @staticmethod
    def find_academic_calendar_by_event_type(academic_year_id, session_number):
        event_type_criteria = "EXAM_SCORES_SUBMISSION_SESS_"+str(session_number)
        return AcademicCalendar.objects.get(academic_year=academic_year_id, event_type=event_type_criteria)

    @staticmethod
    def find_by_academic_year(academic_year_id):
        return AcademicCalendar.objects.filter(academic_year=academic_year_id).order_by('title')

    @staticmethod
    def find_by_academic_year_with_dates(academic_year_id):
        now = timezone.now()
        return AcademicCalendar.objects.filter(academic_year=academic_year_id, start_date__isnull=False, end_date__isnull=False)\
                                        .filter(models.Q(start_date__lte=now, end_date__gte=now) | models.Q(start_date__gte=now, end_date__gte=now))\
                                        .order_by('start_date')

    @staticmethod
    def find_by_id(id):
        return AcademicCalendar.objects.get(pk=id)

    def __str__(self):
        return u"%s %s" % (self.academic_year, self.title)

    def save(self,  *args, **kwargs):
            new = False
            start_date_before_change = None
            end_date_before_change = None
            if self.id is None:
                new = True
            else:
                academic_calendar = AcademicCalendar.objects.get(pk=self.id)
                start_date_before_change = academic_calendar.start_date
                end_date_before_change = academic_calendar.end_date

            academic_calendar=super(AcademicCalendar, self).save(*args, **kwargs)
            academic_year = self.academic_year

            if new:
                offer_year_list = OfferYear.find_offer_years_by_academic_year(academic_year.id)
                for offer_year in offer_year_list:
                    offer_year_calendar=OfferYearCalendar()
                    offer_year_calendar.academic_calendar = self
                    offer_year_calendar.offer_year=offer_year
                    offer_year_calendar.start_date = self.start_date
                    offer_year_calendar.end_date = self.end_date
                    offer_year_calendar.save()
            else:
                if (start_date_before_change is None and end_date_before_change is None ) or ((not start_date_before_change is None and start_date_before_change.strftime( '%d/%m/%Y')) != (not self.start_date is None and self.start_date.strftime( '%d/%m/%Y')) or (not end_date_before_change is None and end_date_before_change.strftime('%d/%m/%Y') != (not self.end_date is None and self.end_date.strftime( '%d/%m/%Y')))) :
                    #Do this only if start_date or end_date changed
                    offer_year_calendar_list = OfferYearCalendar.find_offer_years_by_academic_calendar(self)

                    for offer_year_calendar in offer_year_calendar_list:
                        if offer_year_calendar.customized == True:
                            #an email must be sent to the programme manager
                            programme_managers = ProgrammeManager.objects.filter(faculty=offer_year_calendar.offer_year.structure)
                            if programme_managers and len(programme_managers) > 0:
                                send_mail.send_mail_after_academic_calendar_changes(self,offer_year_calendar, programme_managers)
                        else:
                            offer_year_calendar.start_date = self.start_date
                            offer_year_calendar.end_date = self.end_date
                            offer_year_calendar.save()

            return academic_calendar


class Offer(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed     = models.DateTimeField(null=True)
    acronym     = models.CharField(max_length=15)
    title       = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.acronym = self.acronym.upper()
        super(Offer, self).save(*args, **kwargs)

    @property
    def structure(self):
        return Structure.objects.filter(id=self.id).structure

    @staticmethod
    def find_offer_by_id(id):
        return Offer.objects.get(pk=id)

    def __str__(self):
        return self.acronym


class OfferYear(models.Model):
    external_id   = models.CharField(max_length=100, blank=True, null=True)
    changed       = models.DateTimeField(null=True)
    offer         = models.ForeignKey(Offer)
    academic_year = models.ForeignKey(AcademicYear)
    acronym       = models.CharField(max_length=15)
    title         = models.CharField(max_length=255)
    structure     = models.ForeignKey(Structure)
    parent  = models.ForeignKey('self', blank=True, null=True, related_name='children',db_index=True)

    @staticmethod
    def find_offer_years_by_academic_year(academic_year):
        return OfferYear.objects.filter(academic_year=int(academic_year))

    @staticmethod
    def find_offer_years_by_academic_year_structure(academic_year,structure):
        return OfferYear.objects.filter(academic_year=academic_year, structure=structure).order_by('acronym')

    @staticmethod
    def find_offer_year_by_id(offer_year_id):
        return OfferYear.objects.get(pk=offer_year_id)

    def __str__(self):
        return u"%s - %s" % (self.academic_year, self.offer.acronym)

    @property
    def offer_year_children(self):
        '''
        To find children
        '''
        return  OfferYear.objects.filter(parent=self)

    @property
    def offer_year_sibling(self):
        '''
        To find other focuses
        '''
        if self.parent:
            return OfferYear.objects.filter(parent=self.parent).exclude(id=self.id).exclude()
        return None

    @property
    def is_orientation(self):
        if self.orientation_sibling():
            return True
        else:
            return False

    @property
    def orientation_sibling(self):
        if self.offer:
            offer = Offer.find_offer_by_id(self.offer.id)
            return OfferYear.objects.filter(offer=offer,acronym=self.acronym,academic_year=self.academic_year).exclude(id=self.id)
        return None

    @staticmethod
    def find_all():
        return OfferYear.objects.all()

    def find_offer_year_calendar(self):
        return OfferYearCalendar.objects.filter(offer_year=self,start_date__isnull=False,end_date__isnull=False).order_by('start_date','academic_calendar__title')


class ProgrammeManager(models.Model):
    changed = models.DateTimeField(null=True)
    person  = models.ForeignKey(Person)
    faculty = models.ForeignKey(Structure)

    @staticmethod
    def find_faculty_by_user(user):
        programme_manager = ProgrammeManager.objects.filter(person__user=user).first()
        if programme_manager:
            return programme_manager.faculty
        else:
            return None

    @staticmethod
    def is_programme_manager(user, structure):
        person = Person.objects.get(user=user)
        if user:
            programme_manager = ProgrammeManager.objects.filter(person=person.id, faculty=structure)
            if programme_manager:
                return True
        return False

    def __str__(self):
        return u"%s - %s" % (self.person, self.faculty)


class OfferEnrollment(models.Model):
    external_id     = models.CharField(max_length=100, blank=True, null=True)
    changed         = models.DateTimeField(null=True)
    date_enrollment = models.DateField()
    offer_year      = models.ForeignKey(OfferYear)
    student         = models.ForeignKey(Student)

    def __str__(self):
        return u"%s - %s" % (self.student, self.offer_year)


class OfferYearCalendar(models.Model):
    external_id       = models.CharField(max_length=100, blank=True, null=True)
    changed           = models.DateTimeField(null=True)
    academic_calendar = models.ForeignKey(AcademicCalendar)
    offer_year        = models.ForeignKey(OfferYear)
    event_type        = models.CharField(max_length=50, choices=EVENT_TYPE)
    start_date        = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date          = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    customized        = models.BooleanField(default=False)

    @staticmethod
    def current_session_exam():
        return OfferYearCalendar.objects.filter(event_type__startswith='EXAM_SCORES_SUBMISSION_SESS_')\
                                        .filter(start_date__lte=timezone.now())\
                                        .filter(end_date__gte=timezone.now()).first()

    @staticmethod
    def find_offer_years_by_academic_calendar(academic_calendar):
        return OfferYearCalendar.objects.filter(academic_calendar=int(academic_calendar.id))

    def __str__(self):
        return u"%s - %s - %s" % (self.academic_calendar, self.offer_year, self.event_type)


class LearningUnit(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed     = models.DateTimeField(null=True)
    acronym     = models.CharField(max_length=15)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_year  = models.IntegerField()
    end_year    = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return u"%s - %s" % (self.acronym, self.title)


class Attribution(models.Model):
    FUNCTION_CHOICES = (
        ('COORDINATOR','Coordinator'),
        ('PROFESSOR','Professor'))

    external_id   = models.CharField(max_length=100, blank=True, null=True)
    changed       = models.DateTimeField(null=True)
    start_date    = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date      = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    function      = models.CharField(max_length=15, blank=True, null=True, choices=FUNCTION_CHOICES, default='UNKNOWN')
    learning_unit = models.ForeignKey(LearningUnit)
    tutor         = models.ForeignKey(Tutor)

    def __str__(self):
        return u"%s - %s" % (self.tutor.person, self.function)


class LearningUnitYear(models.Model):
    external_id    = models.CharField(max_length=100, blank=True, null=True)
    changed        = models.DateTimeField(null=True)
    acronym        = models.CharField(max_length=15)
    title          = models.CharField(max_length=255)
    credits        = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    decimal_scores = models.BooleanField(default=False)
    academic_year  = models.ForeignKey(AcademicYear)
    learning_unit  = models.ForeignKey(LearningUnit)

    @staticmethod
    def find_offer_enrollments(learning_unit_year_id):
        learning_unit_enrollment_list= LearningUnitEnrollment.objects.filter(learning_unit_year=learning_unit_year_id)
        offer_list = []
        for lue in learning_unit_enrollment_list:
            offer_list.append(lue.offer_enrollment)
        return offer_list

    @staticmethod
    def find_learning_unit_years_by_academic_year(academic_year):
        return LearningUnitYear.objects.filter(academic_year=int(academic_year))

    @staticmethod
    def find_learning_unit_year_by_id(learning_unit_id) :
        return LearningUnitYear.objects.get(pk=learning_unit_id)

    def __str__(self):
        return u"%s - %s" % (self.academic_year,self.learning_unit)


class LearningUnitEnrollment(models.Model):
    external_id        = models.CharField(max_length=100, blank=True, null=True)
    changed            = models.DateTimeField(null=True)
    date_enrollment    = models.DateField()
    learning_unit_year = models.ForeignKey(LearningUnitYear)
    offer_enrollment   = models.ForeignKey(OfferEnrollment)

    @property
    def student(self):
        return self.offer_enrollment.student

    @property
    def offer(self):
        return self.offer_enrollment.offer_year

    def __str__(self):
        return u"%s - %s" % (self.learning_unit_year, self.offer_enrollment.student)


class SessionExam(models.Model):
    SESSION_STATUS = (
        ('IDLE', _('Idle')),
        ('OPEN', _('Open')),
        ('CLOSED', _('Closed')))

    external_id         = models.CharField(max_length=100, blank=True, null=True)
    changed             = models.DateTimeField(null=True)
    number_session      = models.IntegerField()
    status              = models.CharField(max_length=10,choices=SESSION_STATUS)
    learning_unit_year  = models.ForeignKey(LearningUnitYear)
    offer_year_calendar = models.ForeignKey(OfferYearCalendar)

    @staticmethod
    def current_session_exam():
        offer_calendar = OfferYearCalendar.current_session_exam()
        session_exam = SessionExam.objects.filter(offer_year_calendar=offer_calendar).first()
        return session_exam

    @staticmethod
    def find_session(id):
        return SessionExam.objects.get(pk=id)

    @staticmethod
    def find_sessions_by_tutor(tutor, academic_year):
        learning_units = Attribution.objects.filter(tutor=tutor).values('learning_unit')
        return SessionExam.objects.filter(~models.Q(status='IDLE'))\
                                  .filter(learning_unit_year__academic_year=academic_year)\
                                  .filter(learning_unit_year__learning_unit__in=learning_units)

    @staticmethod
    def find_sessions_by_faculty(faculty, academic_year):
        return SessionExam.objects.filter(~models.Q(status='IDLE'))\
                                  .filter(offer_year_calendar__offer_year__academic_year=academic_year)\
                                  .filter(offer_year_calendar__offer_year__structure=faculty)

    @property
    def offer(self):
        for rec_exam_enrollment in ExamEnrollment.find_exam_enrollments(self):
            return rec_exam_enrollment.learning_unit_enrollment.offer
        return None

    @property
    def progress(self):
        enrollments = list(ExamEnrollment.find_exam_enrollments(self))

        if enrollments:
            progress = 0
            for e in enrollments:
                if e.score_final is not None or e.justification_final is not None:
                    progress = progress +1
            return str(progress) + "/"+ str(len(enrollments))
        else:
            return "0/0"

    def __str__(self):
        return u"%s - %d" % (self.learning_unit_year, self.number_session)


JUSTIFICATION_TYPES = (
        ('ABSENT',_('Absent')),
        ('CHEATING',_('Cheating')),
        ('ILL',_('Ill')),
        ('JUSTIFIED_ABSENCE',_('Justified absence')),
        ('SCORE_MISSING',_('Score missing')))


class ExamEnrollment(models.Model):
    ENCODING_STATUS_LIST = (
        ('SAVED',_('Saved')),
        ('SUBMITTED',_('Submitted')))

    external_id              = models.CharField(max_length=100, blank=True, null=True)
    changed                  = models.DateTimeField(null=True)
    score_draft              = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    score_reencoded          = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    score_final              = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    justification_draft      = models.CharField(max_length=20, blank=True, null=True, choices=JUSTIFICATION_TYPES)
    justification_reencoded  = models.CharField(max_length=20, blank=True, null=True, choices=JUSTIFICATION_TYPES)
    justification_final      = models.CharField(max_length=20, blank=True, null=True, choices=JUSTIFICATION_TYPES)
    encoding_status          = models.CharField(max_length=9, blank=True, null=True, choices=ENCODING_STATUS_LIST)
    session_exam             = models.ForeignKey(SessionExam)
    learning_unit_enrollment = models.ForeignKey(LearningUnitEnrollment)

    @staticmethod
    def calculate_progress(enrollments):
        if enrollments:
            progress = len([e for e in enrollments if e.score_final or e.justification_final]) / len(enrollments)
        else:
            progress = 0
        return progress * 100

    @staticmethod
    def find_exam_enrollments(session_exam):
        enrollments = ExamEnrollment.objects.filter(session_exam=session_exam)\
                                            .order_by('learning_unit_enrollment__offer_enrollment__offer_year__acronym',
                                                      'learning_unit_enrollment__offer_enrollment__student__person__last_name',
                                                      'learning_unit_enrollment__offer_enrollment__student__person__first_name')
        return enrollments

    @staticmethod
    def find_draft_exam_enrollments(session_exam):
        """ Return the enrollments of a session but not the ones already submitted. """
        enrollments = ExamEnrollment.objects.filter(session_exam=session_exam)\
                                            .filter(score_final__isnull=True)\
                                            .filter(models.Q(justification_final__isnull=True) |
                                                    models.Q(justification_final=''))
        return enrollments

    @staticmethod
    def count_encoded_scores(enrollments):
        """ Count the scores that were already encoded but not submitted yet. """
        counter = 0
        for enrollment in enrollments:
            if (enrollment.score_draft or enrollment.justification_draft) \
                    and not enrollment.score_final \
                    and not enrollment.justification_final:
                counter += 1

        return counter

    @staticmethod
    def find_exam_enrollments_to_validate(session_exam):
        enrollments = ExamEnrollment.objects.filter(session_exam=session_exam)\
                                            .filter(~models.Q(score_draft=models.F('score_reencoded')) |
                                                    ~models.Q(justification_draft=models.F('justification_reencoded')))\
                                            .filter(score_final__isnull=True)\
                                            .filter(models.Q(justification_final__isnull=True) |
                                                    models.Q(justification_final=''))
        return enrollments

    def student(self):
        return self.learning_unit_enrollment.student

    @staticmethod
    def justification_label_authorized(is_fac):
        if is_fac:
            return '%s, %s, %s, %s, %s' % (_('Absent'),_('Cheating'), _('Ill'),  _('Justified absence'), _('Score missing'))
        else:
            return '%s, %s, %s' % (_('Absent'), _('Cheating'),_('Score missing'))

    def __str__(self):
        return u"%s - %s" % (self.session_exam, self.learning_unit_enrollment)


class ExamEnrollmentHistory(models.Model):
    exam_enrollment     = models.ForeignKey(ExamEnrollment)
    person              = models.ForeignKey(Person)
    score_final         = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    justification_final = models.CharField(max_length=20, null=True, choices=JUSTIFICATION_TYPES)
    modification_date   = models.DateTimeField(auto_now=True)

    @staticmethod
    def exam_enrollment_historic(user, enrollment, score, justification):
        exam_enrollment_history = ExamEnrollmentHistory()
        exam_enrollment_history.exam_enrollment = enrollment
        exam_enrollment_history.score_final = score
        exam_enrollment_history.justification_final = justification
        exam_enrollment_history.person = Person.find_person_by_user(user)
        exam_enrollment_history.save()
