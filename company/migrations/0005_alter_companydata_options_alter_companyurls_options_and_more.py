# Generated by Django 5.0.2 on 2024-02-19 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_company_primary_color_company_secondary_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companydata',
            options={'verbose_name': 'Company Data', 'verbose_name_plural': 'Company Data'},
        ),
        migrations.AlterModelOptions(
            name='companyurls',
            options={'verbose_name': 'Company Url', 'verbose_name_plural': 'Company Urls'},
        ),
        migrations.CreateModel(
            name='BoardOfDirector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='company/bod/')),
                ('designation', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='board_of_director', to='company.company')),
            ],
        ),
    ]
