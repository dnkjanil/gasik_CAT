# Generated by Django 2.0.7 on 2018-07-29 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ujian', '0006_auto_20180729_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='HasilUjian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_mulai_mengerjakan', models.DateTimeField(auto_now_add=True)),
                ('waktu_selesai_mengerjakan', models.DateTimeField(null=True)),
                ('ujian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ujian.Ujian')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JawabanUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_mengisi', models.DateTimeField(auto_now_add=True)),
                ('huruf_jawaban', models.CharField(max_length=1)),
                ('hasil_ujian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ujian.HasilUjian')),
                ('soal_ujian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ujian.SoalUjian')),
            ],
        ),
    ]
