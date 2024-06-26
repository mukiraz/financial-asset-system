# Generated by Django 5.0.6 on 2024-06-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_asset_assettimedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('currency', models.CharField(max_length=10)),
                ('is_liquid', models.BooleanField(null=True)),
                ('total_value', models.FloatField()),
            ],
        ),
    ]
