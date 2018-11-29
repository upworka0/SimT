# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-07 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_interface', '0013_auto_20180507_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='admin_fp_eletrique_pointe',
            new_name='admin_fp_electrique_pointe',
        ),
        migrations.RenameField(
            model_name='admin',
            old_name='admin_fq_eletrique_pointe',
            new_name='admin_fq_electrique_pointe',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='admin_fq_electrique_pointe_hiver',
        ),
        migrations.AlterField(
            model_name='admin',
            name='admin_id',
            field=models.UUIDField(default=uuid.UUID('c86fa91c-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='autrecharge',
            name='autre_charge_id',
            field=models.UUIDField(default=uuid.UUID('c87265c6-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.UUIDField(default=uuid.UUID('c86fdaae-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_id',
            field=models.UUIDField(default=uuid.UUID('c86f9c4c-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='conducteur',
            name='conducteur_id',
            field=models.UUIDField(default=uuid.UUID('c8715438-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courbedediversitee',
            name='courbe_de_diversite_id',
            field=models.UUIDField(default=uuid.UUID('c8723dee-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='etude',
            name='etude_id',
            field=models.UUIDField(default=uuid.UUID('c870098e-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='logement',
            name='logement_id',
            field=models.UUIDField(default=uuid.UUID('c871cfa8-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='noeud',
            name='noeud_id',
            field=models.UUIDField(default=uuid.UUID('c871a2da-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='penteoriginedediversitee',
            name='pente_origine_diversite_id',
            field=models.UUIDField(default=uuid.UUID('c8724eba-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transformateur',
            name='transformateur_id',
            field=models.UUIDField(default=uuid.UUID('c872124c-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedechauffage',
            name='type_chauffage_id',
            field=models.UUIDField(default=uuid.UUID('c8705aa6-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedeconducteur',
            name='type_conducteur_id',
            field=models.UUIDField(default=uuid.UUID('c87071d0-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedelogement',
            name='type_logement_id',
            field=models.UUIDField(default=uuid.UUID('c871141e-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typedetransformateur',
            name='type_transformateur_id',
            field=models.UUIDField(default=uuid.UUID('c8712e86-5225-11e8-878a-0242ac120003'), primary_key=True, serialize=False),
        ),
    ]
