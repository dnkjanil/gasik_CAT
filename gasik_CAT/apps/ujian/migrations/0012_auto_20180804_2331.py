# Generated by Django 2.0.7 on 2018-08-04 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ujian', '0011_auto_20180802_2030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hasilujian',
            options={'ordering': ('user__username',)},
        ),
    ]
