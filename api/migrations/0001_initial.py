# Generated by Django 3.2.8 on 2021-10-11 10:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('network_app', models.TextField()),
                ('network_campaign', models.TextField(blank=True, null=True)),
                ('network_adgroup', models.TextField(blank=True, null=True)),
                ('taps', models.IntegerField()),
                ('views', models.IntegerField()),
                ('cost', models.FloatField()),
                ('earnings', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ParsedData',
            fields=[
                ('internal_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('app', models.TextField()),
                ('campaign', models.TextField(blank=True, null=True)),
                ('ad_group', models.TextField(blank=True, null=True)),
                ('clicks', models.IntegerField()),
                ('impressions', models.IntegerField()),
                ('ad_spend', models.FloatField()),
                ('revenues', models.FloatField()),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rawdata')),
            ],
        ),
    ]