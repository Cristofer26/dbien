# Generated by Django 4.1.4 on 2023-12-25 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0007_habitacion_precio_registroalojamiento_es_responsable_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pasajero',
            name='reservas',
        ),
        migrations.RemoveField(
            model_name='pasajero',
            name='responsable',
        ),
        migrations.AddField(
            model_name='reserva',
            name='pasajero',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='App1.pasajero'),
        ),
    ]
