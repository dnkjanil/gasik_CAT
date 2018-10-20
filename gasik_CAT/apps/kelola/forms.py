from django import forms


class KelolaMahasiswaForm(forms.Form):
    kata_sandi = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Kata Sandi'
        }
    ))
    nama_lengkap = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nama Lengkap'
        }
    ))
