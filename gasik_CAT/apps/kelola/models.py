from django.db import models

# Create your models here.

# Data Jurusan
class Jurusan(models.Model):
    kode_jurusan = models.CharField(max_length=5)
    nama_jurusan = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_jurusan

class HurufJawaban(models.Model):
    huruf = models.CharField(max_length=1)