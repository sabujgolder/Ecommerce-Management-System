# Generated by Django 3.0.3 on 2020-07-10 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecmsapp', '0007_auto_20200628_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_owner',
            name='prfile_pic',
            field=models.ImageField(blank=True, default='profile1.png', null=True, upload_to=''),
        ),
    ]