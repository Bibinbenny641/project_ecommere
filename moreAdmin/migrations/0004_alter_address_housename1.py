# Generated by Django 4.0.7 on 2022-09-20 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moreAdmin', '0003_remove_address_address1_remove_address_address2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Housename1',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]
