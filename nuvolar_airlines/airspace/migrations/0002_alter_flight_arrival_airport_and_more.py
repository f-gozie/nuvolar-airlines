# Generated by Django 4.0.9 on 2023-02-09 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airspace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='arrival_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_flights', to='airspace.airport'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='departure_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_flights', to='airspace.airport'),
        ),
    ]
