from django.shortcuts import render, HttpResponseRedirect, reverse
import sweetify
from gasik_CAT.apps.authenticate.decorator import admin_required
from django.contrib.auth.models import User

# Create your views here.

# Halaman kelola akun mahasiswa

@admin_required
def kelola_mahasiswa(request):
    if request.method == 'GET':
        # Ambil semua data mahasiswa
        mahasiswas = User.objects.filter(is_superuser=False)
        # Form initial data
        context = {
            'mahasiswas': mahasiswas,
        }
        return render(request, 'kelola_mahasiswa.html', context)
    elif request.method == 'POST':
        pass
    else:
        sweetify.error(request, 'Metode Request Tidak Valid')
        return HttpResponseRedirect(reverse('kelola_mahasiswa'))


