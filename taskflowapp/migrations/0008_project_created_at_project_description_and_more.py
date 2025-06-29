# Generated by Django 5.1.7 on 2025-06-24 16:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskflowapp', '0007_project_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
