# Generated by Django 4.1.4 on 2023-12-25 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0009_alter_reserva_pasajero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='pasajero',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='App1.pasajero'),
        ),
    ]
