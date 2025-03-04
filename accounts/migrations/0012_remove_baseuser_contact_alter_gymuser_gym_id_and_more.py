# Generated by Django 5.1.1 on 2024-11-11 14:48

import accounts.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_gymowner_contact_no_gymuser_contact_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='contact',
        ),
        migrations.AlterField(
            model_name='gymuser',
            name='gym_id',
            field=models.ForeignKey(blank=True, default=accounts.models.GymUser.default_gym_owner, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.gymowner'),
        ),
        migrations.AlterField(
            model_name='gymuser',
            name='trainer_id',
            field=models.ForeignKey(blank=True, default=accounts.models.GymUser.default_trainer, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.trainer'),
        ),
    ]
