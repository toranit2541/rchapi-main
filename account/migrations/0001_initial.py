# Generated by Django 5.0.9 on 2025-01-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=10)),
                ('birthday', models.DateField()),
                ('phonenumber', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=15, null=True)),
                ('first_name', models.CharField(blank=True, max_length=15, null=True)),
                ('last_name', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'verbose_name': 'Auth User',
                'verbose_name_plural': 'Auth User',
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
    ]
