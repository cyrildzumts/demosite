# -*- coding: utf-8 -*-
# Generated by Django 1.10.1a1 on 2016-08-27 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20160827_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, help_text='Texte unique representant la page du produit.', max_length=255, unique=True),
        ),
    ]
