from django import forms


class LoginForm(forms.Form):
    nomor_peserta = forms.CharField(max_length=32, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nomor Peserta'
        }
    ))
    kata_sandi = forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Kata Sandi'
        }
    ))

