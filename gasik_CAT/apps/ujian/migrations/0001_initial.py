# Generated by Django 2.0.7 on 2018-07-29 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoalUjian',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('teks_soal', models.CharField(max_length=255)),
                ('jawaban', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Ujian',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nama_ujian', models.CharField(max_length=50)),
                ('waktu_mulai', models.DateTimeField()),
                ('waktu_selesai', models.DateTimeField()),
                ('waktu_ditambahkan', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='soalujian',
            name='ujian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ujian.Ujian'),
        ),
    ]
