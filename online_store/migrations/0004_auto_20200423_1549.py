# Generated by Django 3.0.4 on 2020-04-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0003_productmanager_salesmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cost',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]