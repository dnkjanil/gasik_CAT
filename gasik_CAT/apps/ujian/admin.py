from django.contrib import admin
from gasik_CAT.apps.ujian.models import Ujian, SoalUjian, JawabanSoal, HasilUjian, JawabanUser
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.urls import path
from django.shortcuts import redirect, render
from io import TextIOWrapper
from django.contrib.auth.models import User
import csv
from gasik_CAT.apps.user_profile.models import ProfilUser
from django.contrib import messages
from django.db import IntegrityError
import datetime
from gasik_CAT.apps.ujian.forms import UjianCSVImportForm

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
            reader = csv.reader(csv_file, delimiter=';')

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
                    except:
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

            # try:
            #     for row in reader:
            #         # Buat user baru
            #         # 0 : Username (nomor peserta), 1: password, 2 : nama peserta, 3: kecamatan, 4 : desa, 5: Formasi, 6 : Paket soal
            #         user = User.objects.create_user(username=row[0], password=row[1])
            #         profil_user = ProfilUser(user=user, nama_peserta=row[2], kecamatan=row[3], desa=row[4], formasi=row[5], paket_soal=row[6])
            #         profil_user.save()
            #     self.message_user(request, "Peserta berhasil ditambahkan")
            #     return redirect("..")
            # except IntegrityError:
            #     self.message_user(request, "Peserta : {} sudah pernah ditambahkan".format(row[0]), level=messages.ERROR)
            #     return redirect("..")
            # except:
            #     self.message_user(request, "Format dokumen tidak valid", level=messages.ERROR)
            #     return redirect("..")

        else:
            form = UjianCSVImportForm()
            payload = {"form": form}
            return render(request, "custom_admin/csv_form.html", payload)

admin.site.register(Ujian, UjianAdmin)
admin.site.register(HasilUjian)
admin.site.register(JawabanUser)