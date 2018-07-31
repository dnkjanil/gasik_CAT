from django import forms



class FormProfil(forms.Form):
    nomor_peserta = forms.CharField(max_length=32, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nomor Peserta',
            'readonly': True
        }
    ))
    nama_peserta = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nama Peserta',
        }
    ))
    kecamatan = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Kecamatan',
        }
    ))
    desa = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Desa',
        }
    ))
    formasi = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Formasi',
        }
    ))

