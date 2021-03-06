from django.contrib import admin
from gasik_CAT.apps.ujian.models import Ujian, SoalUjian, JawabanSoal, HasilUjian, JawabanUser
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.urls import path
from django.shortcuts import redirect, render
from io import TextIOWrapper
import csv
from django.contrib import messages
import datetime
from gasik_CAT.apps.ujian.forms import UjianCSVImportForm
from gasik_CAT.apps.pdfs.models import HasilUjianPDFConfig
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from babel.dates import format_date, format_datetime, format_time
from gasik_CAT.settings import BASE_DIR


class JawabanUserAdmin(admin.ModelAdmin):

    list_display = ["get_username", "get_paket_ujian", "soal_ujian", "waktu_mengisi", "huruf_jawaban"]

    # Hapus hak tambah
    def has_add_permission(self, request):
        return False

    # Hapus hak ubah
    def has_change_permission(self, request, obj=None):
        return False

    # # Hapus hak hapus
    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_username(self, obj):
        return obj.hasil_ujian.user.username

    def get_paket_ujian(self, obj):
        return obj.hasil_ujian.ujian.paket_soal

    get_username.short_description = 'Nomor Peserta'
    get_paket_ujian.short_description = 'Paket Ujian'


class JawabanInLine(NestedStackedInline):
    model = JawabanSoal
    extra = 1
    fk_name = 'soal'

class SoalInline(NestedModelAdmin):
    model = SoalUjian
    extra = 1
    fk_name = 'ujian'
    inlines = [JawabanInLine]
    list_display = ["teks_soal", "huruf_jawaban", "get_paket_soal"]
    ordering = ['ujian__paket_soal']

    def get_paket_soal(self, obj):
        return obj.ujian.paket_soal

    get_paket_soal.short_description = 'Paket Soal '


class UjianAdmin(admin.ModelAdmin):
    model = Ujian
    list_display = ('nama_ujian', 'waktu_mulai', 'waktu_selesai', 'waktu_diubah', 'aktif', 'paket_soal')
    list_filter = ('nama_ujian', 'waktu_mulai', 'waktu_selesai', 'waktu_diubah', 'paket_soal')

    # Custom upload from csv
    change_list_template = 'custom_admin/ujian_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]

        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":

            print(request.POST)
            # Ubah dari bytes ke string
            form = UjianCSVImportForm(request.POST, request.FILES)
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
            reader = csv.reader(csv_file, delimiter='@')

            if form.is_valid():
                # Pastikan bahwa paket soal belum pernah ditambahkan
                try:
                    soal = Ujian.objects.get(paket_soal=form.cleaned_data['paket_soal'])
                except Ujian.DoesNotExist:
                    try:
                        # Tambahkan ujian, soal dan jawaban kedalam basis data
                        # Buat ujian baru
                        ujian = Ujian(nama_ujian=form.cleaned_data['nama_ujian'], paket_soal=form.cleaned_data['paket_soal'], waktu_mulai=datetime.datetime.now(), waktu_selesai=datetime.datetime.now())
                        ujian.save()
                        for row in reader:
                            print(row)
                            # Tambahkan soal yang ada
                            soal = SoalUjian(ujian=ujian, teks_soal=row[0], huruf_jawaban=row[1])
                            soal.save()
                            # Tambahkan pilihan jawaban yang ada
                            pilihan_a = JawabanSoal(soal=soal, teks_jawaban=row[2], huruf='A')
                            pilihan_a.save()
                            pilihan_b = JawabanSoal(soal=soal, teks_jawaban=row[3], huruf='B')
                            pilihan_b.save()
                            pilihan_c = JawabanSoal(soal=soal, teks_jawaban=row[4], huruf='C')
                            pilihan_c.save()
                            pilihan_d = JawabanSoal(soal=soal, teks_jawaban=row[5], huruf='D')
                            pilihan_d.save()
                            pilihan_e = JawabanSoal(soal=soal, teks_jawaban=row[6], huruf='E')
                            pilihan_e.save()
                    except Exception as e:
                        self.message_user(request, "Terdapat kesalahan pada format ujian", level=messages.ERROR)
                        return redirect("..")
                    else:
                        self.message_user(request, "Ujian berhasil ditambahkan")
                        return redirect("..")
                else:
                    self.message_user(request, "Paket soal sudah penah ditambahkan", level=messages.ERROR)
                    return redirect("..")
            else:
                self.message_user(request, "Harap lengkapi borang yang tersedia", level=messages.ERROR)
                return redirect("..")

        else:
            form = UjianCSVImportForm()
            payload = {"form": form}
            return render(request, "custom_admin/csv_form.html", payload)

class HasilUjianAdmin(admin.ModelAdmin):

    list_display = ["get_username", "get_full_name", "get_ujian", "get_waktu_mulai_mengerjakan", "get_selesai_mengerjakan"]
    ordering = ['user__username']

    # Custom list display
    def get_username(self, obj):
        return obj.user.username

    def get_full_name(self, obj):
        return obj.user.profiluser.nama_peserta

    def get_ujian(self, obj):
        return obj.ujian

    def get_waktu_mulai_mengerjakan(self, obj):
        return obj.waktu_mulai_mengerjakan

    def get_selesai_mengerjakan(self, obj):
        return obj.selesai_mengerjakan

    get_username.short_description = 'Nomor Peserta'
    get_full_name.short_description = 'Nama Lengkap'
    get_ujian.short_description = 'Ujian'
    get_waktu_mulai_mengerjakan.short_description = 'Mulai Mengerjakan'
    get_selesai_mengerjakan.short_description = 'Sudah Selesai Mengerjakan'

    # Custom unduh hasil
    change_list_template = 'custom_admin/hasilujian_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('hasil/ujian/semua', self.unduh_semua_hasil_ujian),
        ]

        return my_urls + urls

    def unduh_semua_hasil_ujian(self, request):
        if request.method == 'GET':
            # Semua hasil ujian
            semua_hasil_ujian = HasilUjian.objects.all()

            # Ambil konfigurasi pdf
            konfigurasi_pdf = HasilUjianPDFConfig.objects.filter().last()

            # Buat response http dengan header pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="somefilename.pdf"'

            # Buat objek PDF
            p = canvas.Canvas(response, pagesize=A4)

            # Iterasi tiap hasil ujian
            for hasil_ujian in semua_hasil_ujian:
                p.setFont('Helvetica', 10)
                p.setLineWidth(1)

                # Logo kiri
                p.drawImage('{}/{}/{}'.format(BASE_DIR, 'media', konfigurasi_pdf.logo_kiri), 40, 760, mask='auto', width=80, height=60)
                # Logo kanan
                p.drawImage('{}/{}/{}'.format(BASE_DIR, 'media', konfigurasi_pdf.logo_kanan), 500, 760, mask='auto', width=43, height=55)

                # Garis header
                p.line(40, 750, 560, 750)
                # Header
                p.drawString(210, 800, 'PANITIA UJI KOMPETENSI/SELEKSI')
                p.drawString(170, 785, 'PENGISIAN PENGANGKATAN PERANGKAT DESA')
                p.drawString(210, 770, 'KABUPATEN SRAGEN TAHUN 2018')
                p.drawString(140, 755, 'FAKULTAS EKONOMIKA DAN BISNIS UNIVERSITAS DIPONEGORO')

                # Judul
                p.setFont('Helvetica', 12)
                p.drawString(230, 720, 'HASIL UJIAN TERTULIS')
                p.drawString(200, 700, 'COMPUTER ASSISTED TEST (CAT)')

                # Waktu cetak
                p.setFont('Helvetica', 8)
                p.drawString(252, 685, format_date(datetime.datetime.now(), format='full', locale='id'))

                # Data Peserta
                p.setFont('Helvetica', 12)
                p.drawString(60, 650, 'NAMA PESERTA     :')
                p.drawString(180, 650, hasil_ujian.user.profiluser.nama_peserta)
                p.drawString(60, 630, 'NOMOR PESERTA  :')
                p.drawString(180, 630, hasil_ujian.user.username)
                p.drawString(60, 610, 'KECAMATAN           :')
                p.drawString(180, 610, hasil_ujian.user.profiluser.kecamatan)
                p.drawString(60, 590, 'DESA                        :')
                p.drawString(180, 590, hasil_ujian.user.profiluser.desa)
                p.drawString(60, 570, 'FORMASI                 :')
                p.drawString(180, 570, hasil_ujian.user.profiluser.desa)
                p.drawString(60, 550, 'NILAI                        :')

                # Nilai
                nilai = 0
                soal_ujian = SoalUjian.objects.filter(ujian=hasil_ujian.ujian)
                for soal in soal_ujian:
                    try:
                        jawaban_user = JawabanUser.objects.get(soal_ujian=soal, hasil_ujian=hasil_ujian)
                    except JawabanUser.DoesNotExist:
                        pass
                    else:
                        if soal.huruf_jawaban == jawaban_user.huruf_jawaban:
                            nilai += 1
                        else:
                            pass

                p.drawString(180, 550, str(nilai))

                # TTD Peserta
                p.drawString(80, 450, 'Peserta,')
                p.drawString(77, 380, '({})'.format(hasil_ujian.user.profiluser.nama_peserta))

                # TTD Penguji
                p.drawString(420, 450, 'Pengawas Ujian,')
                p.drawString(410, 380, '(.................................)')

                p.showPage()

            # Simpan semua data dan kembalikan dokumen
            p.save()
            return response


admin.site.register(Ujian, UjianAdmin)
admin.site.register(HasilUjian, HasilUjianAdmin)
admin.site.register(SoalUjian, SoalInline)
admin.site.register(JawabanUser, JawabanUserAdmin)