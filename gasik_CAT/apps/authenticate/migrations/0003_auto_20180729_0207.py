# Generated by Django 2.0.7 on 2018-07-29 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0002_auto_20180729_0132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiluser',
            name='user',
        ),
        migrations.DeleteModel(
            name='ProfilUser',
        ),
    ]
