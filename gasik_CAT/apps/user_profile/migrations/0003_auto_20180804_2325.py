# Generated by Django 2.0.7 on 2018-08-04 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_profiluser_paket_soal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profiluser',
            options={'ordering': ('user__username',)},
        ),
    ]
