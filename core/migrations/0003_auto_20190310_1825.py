# Generated by Django 2.1.7 on 2019-03-10 18:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_photo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='exact_geom',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='photo',
            name='osm_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='place_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='request_public_help',
            field=models.IntegerField(blank=True, choices=[(None, 'N/A'), (1, 'yes'), (2, 'no')], null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='wikidata_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='wikipedia_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='status',
            field=models.IntegerField(choices=[(1, 'pending'), (2, 'suggested'), (10, 'found'), (100, 'no place name'), (200, 'photo should not be associated with a place')], default=1),
        ),
    ]