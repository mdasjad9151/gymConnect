# Generated by Django 5.1.1 on 2024-10-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_gymowner_remove_user_gym_instance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
