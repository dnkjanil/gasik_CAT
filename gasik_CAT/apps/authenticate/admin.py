from django.contrib import admin
from gasik_CAT.apps.user_profile.models import ProfilUser
from django.contrib.auth.models import User
from django.urls import path
import csv
from django.shortcuts import redirect, render
from gasik_CAT.apps.authenticate.forms import UserCSVImportForm
from io import TextIOWrapper
from django.contrib import messages
from django.db import IntegrityError
from gasik_CAT.apps.user_profile.models import ProfilUser

# Unregister user model
admin.site.unregister(User)
class ProfilUserInline(admin.StackedInline):
    model = ProfilUser
    extra = 0
    fields = ["nama_peserta", "kecamatan", "desa", "formasi"]
    min_num = 1

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfilUserInline]
    fields = ["username", "password"]
    list_display = ["username", "get_nama_peserta", "get_kecamatan", "get_desa", "get_formasi"]
    list_filter =  ["username"]

    # Custom list display
    def get_nama_peserta(self, obj):
        return obj.profiluser.nama_peserta

    def get_kecamatan(self, obj):
        return obj.profiluser.kecamatan

    def get_desa(self, obj):
        return obj.profiluser.desa

    def get_formasi(self, obj):
        return obj.profiluser.formasi

    get_nama_peserta.admin_order_field = 'nama_peserta'
    get_nama_peserta.short_description = 'Nama Peserta'

    get_kecamatan.admin_order_field = 'kecamatan'
    get_kecamatan.short_description = 'Kecamatan'

    get_desa.admin_order_field = 'desa'
    get_desa.short_description = 'Desa'

    get_formasi.admin_order_field = 'formasi'
    get_formasi.short_description = 'Formasi'

    # Custom upload from csv
    change_list_template = 'custom_admin/user_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]

        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            # Ubah dari bytes ke string
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
            reader = csv.reader(csv_file, delimiter=',')
            try :
                for row in reader:
                    # Buat user baru
                    user = User.objects.create_user(username=row[0], password=row[1])
                    profil_user = ProfilUser(user=user,nama_peserta=row[2], kecamatan=row[3], desa=row[4], formasi=row[5])
                    profil_user.save()
                self.message_user(request, "Peserta berhasil ditambahkan")
                return redirect("..")
            except IntegrityError:
                self.message_user(request, "Peserta : {} sudah pernah ditambahkan".format(row[0]), level=messages.ERROR)
                return redirect("..")
            except:
                self.message_user(request, "Format dokumen tidak valid", level=messages.ERROR)
                return redirect("..")


        form = UserCSVImportForm()
        payload = {"form": form}
        return render(
            request, "custom_admin/csv_form.html", payload
        )