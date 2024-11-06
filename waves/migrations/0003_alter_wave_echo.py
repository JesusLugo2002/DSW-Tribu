# Generated by Django 5.1.3 on 2024-11-06 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echos', '0002_alter_echo_options'),
        ('waves', '0002_alter_wave_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wave',
            name='echo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waves', to='echos.echo'),
        ),
    ]