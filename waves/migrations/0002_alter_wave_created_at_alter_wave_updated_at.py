# Generated by Django 5.1.2 on 2024-10-30 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waves', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wave',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='wave',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]