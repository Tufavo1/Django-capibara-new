# Generated by Django 5.0.6 on 2024-06-14 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capibara', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telefono',
            field=models.CharField(max_length=12),
        ),
    ]
