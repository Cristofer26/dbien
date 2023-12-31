# Generated by Django 4.1.4 on 2023-12-22 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App1', '0003_encargado_alter_servicio_responsable_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habitacion',
            old_name='pasajeros',
            new_name='capacidad',
        ),
        migrations.AddField(
            model_name='pasajero',
            name='responsable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='administradorhotel',
            name='encargado',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.encargado'),
        ),
        migrations.AlterField(
            model_name='encargado',
            name='persona',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.persona'),
        ),
        migrations.AlterField(
            model_name='habitacion',
            name='numero',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='pasajero',
            name='persona',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.persona'),
        ),
        migrations.RemoveField(
            model_name='pasajero',
            name='reservas',
        ),
        migrations.AlterField(
            model_name='persona',
            name='rut',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='registroalojamiento',
            name='habitacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.habitacion'),
        ),
        migrations.AlterField(
            model_name='registroalojamiento',
            name='pasajero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.pasajero'),
        ),
        migrations.AlterField(
            model_name='registroalojamiento',
            name='servicio',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.servicio'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='enUso',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.pasajero'),
        ),
        migrations.AddField(
            model_name='pasajero',
            name='reservas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.reserva'),
        ),
    ]
