# Generated by Django 3.0.4 on 2020-05-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0008_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='id',
        ),
        migrations.AddField(
            model_name='address',
            name='aId',
            field=models.AutoField(default=2, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
