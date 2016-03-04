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
from django.contrib import admin


class StructureAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'title', 'part_of', 'changed')
    fieldsets = ((None, {'fields': ('acronym','title','part_of','organization')}),)
    raw_id_fields = ('part_of', )
    search_fields = ['acronym']


class Structure(models.Model):
    external_id  = models.CharField(max_length=100, blank=True, null=True)
    changed      = models.DateTimeField(null=True)
    acronym      = models.CharField(max_length=15)
    title        = models.CharField(max_length=255)
    organization = models.ForeignKey('Organization', null=True)
    part_of      = models.ForeignKey('self', null=True, blank=True)

    def children(self):
        return Structure.objects.filter(part_of=self.pk)

    def serializable_object(self):
        obj = {'name': self.acronym, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

    def __str__(self):
        return u"%s - %s" % (self.acronym, self.title)


def find_structures():
    return Structure.objects.all().order_by('acronym')


def find_by_id(structure_id):
    return Structure.objects.get(pk=structure_id)


def find_children(self):
    return Structure.objects.filter(part_of=self).order_by('acronym')


def find_by_organization(organization):
    return Structure.objects.filter(organization=organization, part_of__isnull=True)


def find_tree_by_organization(organization):
    structure = Structure.objects.filter(organization=organization)
    tags = []
    if structure:
        for t in Structure.objects.filter(part_of=structure):
            tags.append(t.serializable_object())
    return tags


def find_structure_hierarchy(struc):
    structure = Structure.objects.get(pk=struc.id)
    tags = []
    if structure:
        for t in Structure.objects.filter(part_of=structure):
            tags.append(t.serializable_object())
    return tags


def find_by_acronym(acronym):
    return Structure.objects.get(acronym=acronym.strip())
