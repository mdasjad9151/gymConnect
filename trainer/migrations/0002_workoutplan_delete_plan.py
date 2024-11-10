# Generated by Django 5.1.1 on 2024-11-10 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_gymowner_contact_no_gymuser_contact_no'),
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday_workout', models.TextField(blank=True)),
                ('tuesday_workout', models.TextField(blank=True)),
                ('wednesday_workout', models.TextField(blank=True)),
                ('thursday_workout', models.TextField(blank=True)),
                ('friday_workout', models.TextField(blank=True)),
                ('saturday_workout', models.TextField(blank=True)),
                ('breakfast', models.TextField(blank=True)),
                ('lunch', models.TextField(blank=True)),
                ('dinner', models.TextField(blank=True)),
                ('preworkout_diet', models.TextField(blank=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.gymuser')),
            ],
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
    ]