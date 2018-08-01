from django.contrib import admin
from gasik_CAT.apps.ujian.models import Ujian, SoalUjian, JawabanSoal, HasilUjian, JawabanUser
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

#admin.site.register(Ujian)
#admin.site.register(SoalUjian)


class JawabanInLine(NestedStackedInline):
    model = JawabanSoal
    extra = 1
    fk_name = 'soal'

class SoalInline(NestedStackedInline):
    model = SoalUjian
    extra = 1
    fk_name = 'ujian'
    inlines = [JawabanInLine]

class UjianAdmin(NestedModelAdmin):
    model = Ujian
    list_display = ('nama_ujian', 'waktu_mulai', 'waktu_selesai', 'waktu_diubah', 'aktif', 'paket_soal')
    list_filter = ('nama_ujian', 'waktu_mulai', 'waktu_selesai', 'waktu_diubah', 'paket_soal')
    inlines = [SoalInline]



admin.site.register(Ujian, UjianAdmin)
admin.site.register(HasilUjian)
admin.site.register(JawabanUser)