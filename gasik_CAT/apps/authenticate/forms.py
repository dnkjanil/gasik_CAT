from django import forms


class LoginForm(forms.Form):
    nim = forms.CharField(max_length=32, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nomor Induk Mahasiswa'
        }
    ))
    kata_sandi = forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Kata Sandi'
        }
    ))

class UserCSVImportForm(forms.Form):
    csv_file = forms.FileField()


# Login form admin
class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=32, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ))
    kata_sandi = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Kata Sandi'
        }
    ))

