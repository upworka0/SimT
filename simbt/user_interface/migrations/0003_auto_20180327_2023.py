# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-27 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_interface', '0002_auto_20180327_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='admin_id',
            field=models.UUIDField(default=uuid.UUID('bc8627b4-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='autrecharge',
            name='autre_charge_id',
            field=models.UUIDField(default=uuid.UUID('bc8825d2-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.UUIDField(default=uuid.UUID('bc86426c-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='conducteur',
            name='conducteur_id',
            field=models.UUIDField(default=uuid.UUID('bc877984-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courbedediversitee',
            name='courbe_de_diversite_id',
            field=models.UUIDField(default=uuid.UUID('bc880782-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='etude',
            name='etude_id',
            field=models.UUIDField(default=uuid.UUID('bc86b008-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='logement',
            name='logement_id',
            field=models.UUIDField(default=uuid.UUID('bc87bb06-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='noeud',
            name='noeud_id',
            field=models.UUIDField(default=uuid.UUID('bc87a012-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='penteoriginedediversitee',
            name='pente_origine_diversite_id',
            field=models.UUIDField(default=uuid.UUID('bc88168c-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transformateur',
            name='transformateur_id',
            field=models.UUIDField(default=uuid.UUID('bc87e284-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedechauffage',
            name='type_chauffage_id',
            field=models.UUIDField(default=uuid.UUID('bc86ede8-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedeconducteur',
            name='type_conducteur_id',
            field=models.UUIDField(default=uuid.UUID('bc86fb4e-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedelogement',
            name='type_logement_id',
            field=models.UUIDField(default=uuid.UUID('bc8736cc-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedetransformateur',
            name='type_transformateur_id',
            field=models.UUIDField(default=uuid.UUID('bc87457c-31fc-11e8-87ca-0242ac120003'), primary_key=True, serialize=False),
        ),
    ]