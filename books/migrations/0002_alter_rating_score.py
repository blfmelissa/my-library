# Generated by Django 3.2.12 on 2024-12-04 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.SmallIntegerField(),
        ),
    ]
