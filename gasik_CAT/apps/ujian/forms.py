from django import forms

class JawabanUserForm(forms.Form):

    daftar_pilihan = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(JawabanUserForm, self).__init__(*args, **kwargs)
        self.fields['daftar_pilihan'].widget = forms.RadioSelect()
        self.fields['daftar_pilihan'].choices = self.choices


class UjianCSVImportForm(forms.Form):
    paket_soal = forms.CharField(max_length=5)
    nama_ujian = forms.CharField(max_length=50)
    csv_file = forms.FileField()
