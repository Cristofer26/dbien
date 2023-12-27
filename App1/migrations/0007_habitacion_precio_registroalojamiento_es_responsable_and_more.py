# Generated by Django 4.1.4 on 2023-12-25 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0006_remove_encargado_persona_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitacion',
            name='precio',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='registroalojamiento',
            name='es_responsable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registroalojamiento',
            name='habitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.habitacion'),
        ),
        migrations.AlterField(
            model_name='registroalojamiento',
            name='pasajero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.pasajero'),
        ),
        migrations.AlterField(
            model_name='registroalojamiento',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.servicio'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicios', to='App1.pasajero'),
        ),
    ]