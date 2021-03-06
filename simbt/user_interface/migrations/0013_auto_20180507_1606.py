# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-07 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_interface', '0012_auto_20180507_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.UUIDField(default=uuid.UUID('8a9a5eee-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='admin',
            name='admin_id',
            field=models.UUIDField(default=uuid.UUID('8a9a7370-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='autrecharge',
            name='autre_charge_id',
            field=models.UUIDField(default=uuid.UUID('8a9cbbbc-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.UUIDField(default=uuid.UUID('8a9aaca0-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='conducteur',
            name='conducteur_id',
            field=models.UUIDField(default=uuid.UUID('8a9bc752-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courbedediversitee',
            name='courbe_de_diversite_id',
            field=models.UUIDField(default=uuid.UUID('8a9c94f2-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='etude',
            name='etude_id',
            field=models.UUIDField(default=uuid.UUID('8a9ad202-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='logement',
            name='logement_id',
            field=models.UUIDField(default=uuid.UUID('8a9c2314-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='noeud',
            name='noeud_id',
            field=models.UUIDField(default=uuid.UUID('8a9c03fc-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='penteoriginedediversitee',
            name='pente_origine_diversite_id',
            field=models.UUIDField(default=uuid.UUID('8a9ca6f4-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transformateur',
            name='transformateur_id',
            field=models.UUIDField(default=uuid.UUID('8a9c6482-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedechauffage',
            name='type_chauffage_id',
            field=models.UUIDField(default=uuid.UUID('8a9b1118-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedeconducteur',
            name='type_conducteur_id',
            field=models.UUIDField(default=uuid.UUID('8a9b2392-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedelogement',
            name='type_logement_id',
            field=models.UUIDField(default=uuid.UUID('8a9b9fe8-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedetransformateur',
            name='type_transformateur_id',
            field=models.UUIDField(default=uuid.UUID('8a9bb140-5210-11e8-bb74-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='admin',
            name='company',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_interface.Company'),
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_interface.Company'),
        ),
    ]
