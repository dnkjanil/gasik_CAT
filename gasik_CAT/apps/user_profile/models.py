from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfilUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    nama_peserta = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    desa = models.CharField(max_length=50)
    formasi = models.CharField(max_length=50)


    def __str__(self):
        return self.user.username