# Generated by Django 5.1.1 on 2024-11-08 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_gymuser_gym_id_alter_gymuser_trainer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymowner',
            name='contact',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
