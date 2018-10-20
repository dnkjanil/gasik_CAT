from django.shortcuts import render,HttpResponse, HttpResponseRedirect, reverse
from gasik_CAT.apps.authenticate.forms import LoginForm, AdminLoginForm
from django.contrib.auth import authenticate, login, logout
import sweetify
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_login(request):
    if request.method == "GET" :
        # Contexts
        context = {
            'form': LoginForm()
        }
        return render(request=request,template_name='login.html',context=context)

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['nim'],password=form.cleaned_data['kata_sandi'])
            if (user is not None) and (not user.is_superuser):
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('user_profile'))
            else:
                sweetify.error(request, 'Kombinasi NIM dan Kata Sandi Salah')
                return HttpResponseRedirect(reverse('user_login'))
        else:
            sweetify.error(request, 'Data yang Dimasukkan Tidak Valid')
            return HttpResponseRedirect(reverse('user_login'))
    else:
        sweetify.error(request, 'Metode Request Tidak Valid')
        return HttpResponseRedirect(reverse('user_login'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

# Login admin
def admin_login(request):
    if request.method == "GET" :
        # Contexts
        context = {
            'form': AdminLoginForm()
        }
        return render(request=request,template_name='admin_login.html',context=context)

    elif request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['kata_sandi'])
            if (user is not None) and (user.is_superuser):
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('user_profile'))
            else:
                sweetify.error(request, 'Kombinasi username dan kata sandi salah')
                return HttpResponseRedirect(reverse('admin_login'))
        else:
            sweetify.error(request, 'Data yang Dimasukkan Tidak Valid')
            return HttpResponseRedirect(reverse('admin_login'))
    else:
        sweetify.error(request, 'Metode Request Tidak Valid')
        return HttpResponseRedirect(reverse('admin_login'))

