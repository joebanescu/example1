# Generated by Django 3.2.8 on 2021-10-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parseddata',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]