# Generated by Django 3.0.4 on 2020-05-10 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0012_auto_20200510_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='sex',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
