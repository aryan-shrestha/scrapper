# Generated by Django 5.0.2 on 2024-02-22 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_watchlist_user'),
        ('company', '0008_alter_companydata_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='companies',
            field=models.ManyToManyField(related_name='companies', to='company.company'),
        ),
    ]