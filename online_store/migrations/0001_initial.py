# Generated by Django 3.0.4 on 2020-03-23 11:03

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('cId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=500)),
                ('taxNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('dId', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=500)),
                ('IsDelivered', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pId', models.AutoField(primary_key=True, serialize=False)),
                ('isActive', models.NullBooleanField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('cost', models.FloatField()),
                ('name', models.CharField(max_length=50)),
                ('modelNo', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('warrantyStatus', models.IntegerField()),
                ('disturbuterInfo', models.CharField(max_length=100)),
                ('categoryName', models.CharField(max_length=50)),
                ('listedDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('bId', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('totalPrice', models.FloatField()),
                ('purchasedDate', models.DateField()),
                ('isPurchased', models.NullBooleanField(verbose_name=False)),
                ('cId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Client')),
                ('pId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Product')),
            ],
            options={
                'unique_together': {('bId', 'cId')},
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('isCustomer', models.NullBooleanField(default=True)),
                ('isProductManager', models.NullBooleanField(default=False)),
                ('isSalesManager', models.NullBooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('iId', models.AutoField(primary_key=True, serialize=False)),
                ('bId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Basket')),
                ('cId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Client')),
                ('dId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Delivery')),
            ],
            options={
                'unique_together': {('iId', 'bId', 'dId', 'cId')},
            },
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('fId', models.AutoField(primary_key=True, serialize=False)),
                ('cId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Client')),
                ('pId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_store.Product')),
            ],
            options={
                'unique_together': {('fId', 'cId')},
            },
        ),
    ]
