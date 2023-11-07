# Generated by Django 4.2.7 on 2023-11-07 18:21

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.CharField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=2, message='Username should contail at least 2 characters!')])),
                ('slug', models.SlugField(unique=True)),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(limit_value=2, message='First name should contail at least 2 characters!')])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(limit_value=2, message='Last name should contail at least 2 characters!')])),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('links', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
