# Generated by Django 5.0.2 on 2024-02-18 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0002_alter_companyurls_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyurls',
            name='company',
        ),
        migrations.DeleteModel(
            name='CompanyData',
        ),
        migrations.DeleteModel(
            name='CompanyUrls',
        ),
    ]
