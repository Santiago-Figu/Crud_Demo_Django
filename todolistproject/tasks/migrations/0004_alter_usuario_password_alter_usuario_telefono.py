# Generated by Django 5.1.7 on 2025-03-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_usuario_task_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.TextField(blank=True, null=True),
        ),
    ]
