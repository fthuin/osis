# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 18:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20160303_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='academiccalendar',
            name='event_type',
            field=models.CharField(choices=[('ACADEMIC_YEAR', 'Academic Year'), ('DISSERTATIONS_SUBMISSION_SESS_1', 'Submission of academic dissertations - exam session 1'), ('DISSERTATIONS_SUBMISSION_SESS_2', 'Submission of academic dissertations - exam session 2'), ('DISSERTATIONS_SUBMISSION_SESS_3', 'Submission of academic dissertations - exam session 3'), ('EXAM_SCORES_SUBMISSION_SESS_1', 'Submission of exam scores - exam session 1'), ('EXAM_SCORES_SUBMISSION_SESS_2', 'Submission of exam scores - exam session 2'), ('EXAM_SCORES_SUBMISSION_SESS_3', 'Submission of exam scores - exam session 3'), ('DELIBERATIONS_SESS_1', 'Deliberations - exam session 1'), ('DELIBERATIONS_SESS_2', 'Deliberations - exam session 2'), ('DELIBERATIONS_SESS_3', 'Deliberations - exam session 3'), ('EXAM_SCORES_DIFFUSION_SESS_1', 'Diffusion of exam scores - exam session 1'), ('EXAM_SCORES_DIFFUSION_SESS_2', 'Diffusion of exam scores - exam session 2'), ('EXAM_SCORES_DIFFUSION_SESS_3', 'Diffusion of exam scores - exam session 3'), ('EXAM_ENROLLMENTS_SESS_1', 'Exam enrollments - exam session 1'), ('EXAM_ENROLLMENTS_SESS_2', 'Exam enrollments - exam session 2'), ('EXAM_ENROLLMENTS_SESS_3', 'Exam enrollments - exam session 3')], default='null', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offeryearcalendar',
            name='event_type',
            field=models.CharField(choices=[('ACADEMIC_YEAR', 'Academic Year'), ('DISSERTATIONS_SUBMISSION_SESS_1', 'Submission of academic dissertations - exam session 1'), ('DISSERTATIONS_SUBMISSION_SESS_2', 'Submission of academic dissertations - exam session 2'), ('DISSERTATIONS_SUBMISSION_SESS_3', 'Submission of academic dissertations - exam session 3'), ('EXAM_SCORES_SUBMISSION_SESS_1', 'Submission of exam scores - exam session 1'), ('EXAM_SCORES_SUBMISSION_SESS_2', 'Submission of exam scores - exam session 2'), ('EXAM_SCORES_SUBMISSION_SESS_3', 'Submission of exam scores - exam session 3'), ('DELIBERATIONS_SESS_1', 'Deliberations - exam session 1'), ('DELIBERATIONS_SESS_2', 'Deliberations - exam session 2'), ('DELIBERATIONS_SESS_3', 'Deliberations - exam session 3'), ('EXAM_SCORES_DIFFUSION_SESS_1', 'Diffusion of exam scores - exam session 1'), ('EXAM_SCORES_DIFFUSION_SESS_2', 'Diffusion of exam scores - exam session 2'), ('EXAM_SCORES_DIFFUSION_SESS_3', 'Diffusion of exam scores - exam session 3'), ('EXAM_ENROLLMENTS_SESS_1', 'Exam enrollments - exam session 1'), ('EXAM_ENROLLMENTS_SESS_2', 'Exam enrollments - exam session 2'), ('EXAM_ENROLLMENTS_SESS_3', 'Exam enrollments - exam session 3')], default='null', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programmemanager',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.Structure'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='label',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]