# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-22 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='entity_type',
        ),
        migrations.AddField(
            model_name='workspace',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='workspace',
            name='location_lat',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workspace',
            name='location_long',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workspace',
            name='maxsize',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='workspace',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Service'),
        ),
        migrations.AlterModelTable(
            name='workspace',
            table='workspace',
        ),
    ]