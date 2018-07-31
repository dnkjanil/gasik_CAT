from django.urls import path

from gasik_CAT.apps.ujian.views import informasi_ujian, mulai_ujian, lihat_hasil_ujian

urlpatterns = [
    path('', informasi_ujian, name='informasi_ujian'),
    path('mulai/<slug:id_ujian>/<slug:nomor_soal>', mulai_ujian, name='mulai_ujian'),
    path('lihat/hasil/', lihat_hasil_ujian, name='lihat_hasil_ujian'),
]