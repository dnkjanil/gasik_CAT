from django.db import models

# Create your models here.

class HasilUjianPDFConfig(models.Model):
    logo_kiri = models.ImageField(upload_to='pdf/logo')
    logo_kanan = models.ImageField(upload_to='pdf/logo')
    teks_kop = models.CharField(max_length=255)
    judul = models.CharField(max_length=255)
    waktu_diubah = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.judul