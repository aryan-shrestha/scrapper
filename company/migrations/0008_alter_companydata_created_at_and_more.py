# Generated by Django 5.0.2 on 2024-02-22 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_floorsheet_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydata',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companydata',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]