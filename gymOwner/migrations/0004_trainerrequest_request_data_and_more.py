# Generated by Django 5.1.1 on 2024-11-07 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymOwner', '0003_delete_userrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainerrequest',
            name='request_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trainerrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]