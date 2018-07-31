from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
import sweetify
from gasik_CAT.apps.user_profile.models import ProfilUser
from gasik_CAT.apps.user_profile.forms import FormProfil

# Create your views here.

@login_required()
def user_profile(request):
    if request.method == "GET":
        # Form initial data
        initial = {
            'nomor_peserta': request.user.username,
            'nama_peserta': request.user.profiluser.nama_peserta,
            'kecamatan': request.user.profiluser.kecamatan,
            'desa': request.user.profiluser.desa,
            'formasi': request.user.profiluser.formasi
        }
        context = {
            'form': FormProfil(initial=initial)
        }
        return render(request=request, template_name='profil.html', context=context)
    elif request.method == "POST":
        form = FormProfil(request.POST)
        if form.is_valid():
            # Simpan data
            request.user.profiluser.nama_peserta = form.cleaned_data['nama_peserta']
            request.user.profiluser.kecamatan = form.cleaned_data['kecamatan']
            request.user.profiluser.desa = form.cleaned_data['desa']
            request.user.profiluser.formasi = form.cleaned_data['formasi']
            request.user.profiluser.save()
            sweetify.success(request, 'Data profil berhasil disimpan')
            return HttpResponseRedirect(reverse('user_profile'))
        else:
            sweetify.error(request, 'Harap lengkapi borang yang ada')
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        sweetify.error(request, 'Metode request tidak valid')
        return HttpResponseRedirect(reverse('user_profile'))
