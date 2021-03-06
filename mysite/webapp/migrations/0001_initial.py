# Generated by Django 2.0.6 on 2018-06-10 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MeasureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('measurements', models.ManyToManyField(to='webapp.MeasureType')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.SensorType'),
        ),
        migrations.AddField(
            model_name='entry',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Sensor'),
        ),
    ]
