# Generated by Django 5.1.2 on 2024-11-24 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0002_alter_credito_monto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prestamos.cliente'),
        ),
    ]
