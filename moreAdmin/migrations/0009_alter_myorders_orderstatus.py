# Generated by Django 4.0.7 on 2022-09-21 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moreAdmin', '0008_alter_myorders_orderstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myorders',
            name='orderstatus',
            field=models.CharField(max_length=50),
        ),
    ]
