# Generated by Django 2.1.5 on 2019-11-03 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_patient_rfid'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='finger',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pharmacist',
            name='finger',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='prescription',
            name='finger',
            field=models.CharField(max_length=10, null=True),
        ),
    ]