from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Ujian(models.Model):
    id = models.AutoField(primary_key=True)
    nama_ujian = models.CharField(max_length=50)
    waktu_mulai = models.DateTimeField()
    waktu_selesai = models.DateTimeField()
    waktu_diubah = models.DateTimeField(auto_now=True)
    aktif = models.BooleanField(default=False)
    paket_soal = models.CharField(max_length=5)

    def __str__(self):
        return self.nama_ujian

class SoalUjian(models.Model):
    id = models.AutoField(primary_key=True)
    ujian = models.ForeignKey(Ujian, on_delete=models.CASCADE)
    teks_soal = models.TextField()
    huruf_jawaban = models.CharField(max_length=1)

    def __str__(self):
        return self.teks_soal

class JawabanSoal(models.Model):
    soal = models.ForeignKey(SoalUjian, on_delete=models.CASCADE)
    teks_jawaban = models.TextField()
    huruf = models.CharField(max_length=1)

    def __str__(self):
        return self.huruf + ':' + self.teks_jawaban

class HasilUjian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ujian = models.ForeignKey(Ujian, on_delete=models.CASCADE)
    waktu_mulai_mengerjakan = models.DateTimeField(auto_created=True)
    # Waktu selesai diisi setelah user menekan tombol submit
    selesai_mengerjakan = models.BooleanField(default=False)

    def __str__(self):
        return self.ujian.nama_ujian + ' : ' + self.user.username

    class Meta:
        ordering = ('user__username',)

class JawabanUser(models.Model):
     soal_ujian = models.ForeignKey(SoalUjian, on_delete=models.CASCADE)
     hasil_ujian = models.ForeignKey(HasilUjian, on_delete=models.CASCADE)
     waktu_mengisi = models.DateTimeField(auto_now=True)
     huruf_jawaban = models.CharField(max_length=1)

     def __str__(self):
         return self.huruf_jawaban
