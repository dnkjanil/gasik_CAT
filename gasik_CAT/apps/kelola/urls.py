from django.urls import path

from gasik_CAT.apps.kelola.views import kelola_mahasiswa

urlpatterns = [
    path('mahasiswa', kelola_mahasiswa, name='kelola_mahasiswa'),
]