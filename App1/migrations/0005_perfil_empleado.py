# Generated by Django 4.1.4 on 2023-12-23 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0004_rename_pasajeros_habitacion_capacidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('detalles', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_contratacion', models.DateField()),
                ('perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App1.perfil')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App1.persona')),
            ],
        ),
    ]
