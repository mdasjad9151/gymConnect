# Generated by Django 5.1.1 on 2024-11-09 18:24

import accounts.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_gymowner_contact_baseuser_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='contact_no',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='gym_id',
            field=models.ForeignKey(blank=True, default=accounts.models.Trainer.default_gym_owner, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.gymowner'),
        ),
    ]
