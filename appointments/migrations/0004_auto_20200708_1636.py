# Generated by Django 3.0.8 on 2020-07-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_appointments_aid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='aid',
            field=models.CharField(max_length=50),
        ),
    ]
