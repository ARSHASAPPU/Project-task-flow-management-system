# Generated by Django 5.1.7 on 2025-06-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskflowapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Team Member', 'Team Member')], max_length=20)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
