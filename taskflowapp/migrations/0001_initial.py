# Generated by Django 5.1.7 on 2025-06-22 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='admin', max_length=150, unique=True)),
                ('password', models.CharField(default='admin123', max_length=128)),
                ('secret_code', models.CharField(default='000000', help_text='6-digit admin secret code', max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
