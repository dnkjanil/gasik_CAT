from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
import sweetify
from gasik_CAT.apps.ujian.models import Ujian, SoalUjian, HasilUjian, JawabanSoal, JawabanUser
import pytz
import datetime
from gasik_CAT.apps.ujian.forms import JawabanUserForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from babel.dates import format_date, format_datetime, format_time
from gasik_CAT.apps.pdfs.models import HasilUjianPDFConfig

# Create your views here.

@login_required()
def informasi_ujian(request):
    if request.method == "GET":
        # Data Ujian diambil yang aktif dan paling baru
        ujian = Ujian.objects.filter(aktif=True).last()
        # Pastikan ada ujian yang aktif
        if (ujian):
            # Jumlah soal
            soal = SoalUjian.objects.filter(ujian=ujian)
            context = {
                'id_ujian': ujian.pk,
                'nama_ujian': ujian.nama_ujian,
                'waktu_mulai': ujian.waktu_mulai,
                'waktu_pengerjaan': int((ujian.waktu_selesai - ujian.waktu_mulai).total_seconds() / 60),
                'bisa_dimulai': (datetime.datetime.now() <= ujian.waktu_selesai.replace(tzinfo=None) + datetime.timedelta(hours=7)) and (datetime.datetime.now() >= ujian.waktu_mulai.replace(tzinfo=None) + datetime.timedelta(hours=7)),
                'waktu_selesai': ujian.waktu_selesai,
                'jumlah_soal': soal.count(),
            }
            return render(request=request, template_name='ujian.html', context=context)
        else:
            sweetify.error(request, 'Maaf, belum ada ujian yang tersedia')
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        sweetify.error(request, 'Metode request tidak valid')
        return HttpResponseRedirect(reverse('user_profile'))

@login_required()
def mulai_ujian(request, id_ujian, nomor_soal):
    try:
        # Periksa kode ujian
        ujian = Ujian.objects.get(pk=id_ujian)
    except Ujian.DoesNotExist:
        sweetify.error(request, 'Ujian tidak dapat ditemukan')
        return HttpResponseRedirect(reverse('informasi_ujian'))
    else:
        # Periksa waktu ujian
        if (datetime.datetime.now() <= ujian.waktu_selesai.replace(tzinfo=None) + datetime.timedelta(hours=7)) and (datetime.datetime.now() >= ujian.waktu_mulai.replace(tzinfo=None) + datetime.timedelta(hours=7)):
            try:
                # Periksa apakah user telah enroll
                hasil_ujian = HasilUjian.objects.get(user=request.user, ujian=ujian)
            except HasilUjian.DoesNotExist:
                # Enroll user kedalam ujian
                hasil_ujian = HasilUjian(user=request.user, ujian=ujian)
                hasil_ujian.save()

            # Periksa apakah user telah mengerjakan ujian
            if not hasil_ujian.waktu_selesai_mengerjakan:
                # Periksa kode soal
                try:
                    soal = SoalUjian.objects.filter(ujian=ujian)[int(nomor_soal)-1:int(nomor_soal)]
                except AssertionError:
                    # Jika nomor soal tidak valid
                    sweetify.error(request, 'Soal tidak dapat ditemukan')
                    return HttpResponseRedirect(reverse('informasi_ujian'))
                else:
                    if soal.count() != 0:
                        if request.method == "GET":
                            # Context
                            jawaban_soal = JawabanSoal.objects.filter(soal=soal[0])
                            try :
                                # Ambil jawaban user
                                jawaban_user = JawabanUser.objects.get(hasil_ujian=hasil_ujian, soal_ujian=soal[0])
                            except JawabanUser.DoesNotExist:
                                jawaban_terpilih = ''
                            else:
                                jawaban_terpilih = jawaban_user.huruf_jawaban

                            tersedia_soal_berikutnya = SoalUjian.objects.filter(ujian=ujian)[int(nomor_soal):int(nomor_soal) + 1].count() != 0
                            # Soal berikutnya
                            if tersedia_soal_berikutnya :
                                nomor_soal_berikutnya = int(nomor_soal) + 1
                                nomor_soal_sebelumnya = int(nomor_soal) - 1
                            else:
                                nomor_soal_sebelumnya = int(nomor_soal) - 1
                                nomor_soal_berikutnya = int(nomor_soal)

                            context = {
                                'soal': soal[0],
                                'nomor_soal': nomor_soal,
                                'id_ujian': id_ujian,
                                'daftar_jawaban': JawabanSoal.objects.filter(soal=soal[0]),
                                'form': JawabanUserForm(initial={'daftar_pilihan': jawaban_terpilih}, choices=tuple((jawaban.huruf, jawaban.teks_jawaban) for jawaban in jawaban_soal)),
                                # Periksa soal berikutnya
                                'tersedia_soal_berikutnya': tersedia_soal_berikutnya,
                                'nomor_soal_berikutnya': nomor_soal_berikutnya,
                                'nomor_soal_sebelumnya': nomor_soal_sebelumnya,
                                'sisa_detik': ((ujian.waktu_selesai.replace(tzinfo=None) + datetime.timedelta(hours=7))- datetime.datetime.now()).total_seconds()
                            }
                            return render(request=request, template_name='mulai_ujian.html', context=context)
                        elif request.method == "POST":
                            jawaban_soal = JawabanSoal.objects.filter(soal=soal[0])
                            form = JawabanUserForm(request.POST, choices=tuple((jawaban.huruf, jawaban.teks_jawaban) for jawaban in jawaban_soal))
                            # Periksa apakah form valid
                            if form.is_valid():
                                try:
                                    # Ambil Jawaban user
                                    jawaban_user = JawabanUser.objects.get(hasil_ujian=hasil_ujian, soal_ujian=soal[0])
                                except JawabanUser.DoesNotExist:
                                    # Buat jawaban baru
                                    jawaban_user = JawabanUser(hasil_ujian=hasil_ujian, soal_ujian=soal[0], huruf_jawaban=form.cleaned_data['daftar_pilihan'])
                                    jawaban_user.save()
                                else:
                                    # Update jawaban user
                                    jawaban_user.huruf_jawaban = form.cleaned_data['daftar_pilihan']
                                    jawaban_user.save()

                                # Arahkan ke halaman tujuan
                                # Halaman berikutnya
                                if 'tombol_berikutnya' in request.POST:
                                    return HttpResponseRedirect(reverse(mulai_ujian, kwargs={'id_ujian':id_ujian, 'nomor_soal': int(nomor_soal) + 1}))
                                # Halaman sebelumnya
                                elif 'tombol_sebelumnya' in request.POST:
                                    return HttpResponseRedirect(reverse(mulai_ujian, kwargs={'id_ujian': id_ujian, 'nomor_soal': int(nomor_soal) - 1}))
                                elif 'tombol_selesai' in request.POST:
                                    # Ubah status pengerjaan soal user
                                    hasil_ujian.waktu_selesai_mengerjakan = datetime.datetime.now()
                                    hasil_ujian.save()
                                    return HttpResponseRedirect(reverse('informasi_ujian'))
                            else:
                                sweetify.error(request, 'Mohon isi jawaban')
                                return HttpResponseRedirect(reverse('informasi_ujian'))
                        else:
                            sweetify.error(request, 'Metode request tidak valid')
                            return HttpResponseRedirect(reverse('user_profile'))
                    else:
                        sweetify.error(request, 'Soal tidak dapat ditemukan')
                        return HttpResponseRedirect(reverse('informasi_ujian'))
            else:
                sweetify.info(request, 'Ujian telah selesai dikerjakan')
                return HttpResponseRedirect(reverse('informasi_ujian'))
        else:
            try:
                # Periksa apakah user telah enroll
                hasil_ujian = HasilUjian.objects.get(user=request.user, ujian=ujian)
            except HasilUjian.DoesNotExist:
                sweetify.error(request, 'Ujian telah selesai atau belum dapat diakses')
                return HttpResponseRedirect(reverse('informasi_ujian'))
            else:
                # Apabila waktu pengerjaan selesai
                if hasil_ujian.waktu_selesai_mengerjakan:
                    sweetify.info(request, 'Ujian telah selesai dikerjakan')
                    return HttpResponseRedirect(reverse('informasi_ujian'))
                else:
                    hasil_ujian.waktu_selesai_mengerjakan = datetime.datetime.now()
                    hasil_ujian.save()
                    sweetify.error(request, 'Ujian telah selesai atau belum dapat diakses')
                    return HttpResponseRedirect(reverse('informasi_ujian'))

@login_required()
def lihat_hasil_ujian(request):
    if request.method == "GET":
        # Data Ujian diambil yang aktif dan paling baru
        ujian = Ujian.objects.filter(aktif=True).last()
        # Pastikan ada ujian yang aktif
        if (ujian):
            # Periksa apakah user telah mengerjakan ujian
            try:
                hasil_ujian = HasilUjian.objects.get(user=request.user, ujian=ujian)
            except HasilUjian.DoesNotExist:
                # Periksa apakah ujian masih valid
                if  ((datetime.datetime.now() <= ujian.waktu_selesai.replace(tzinfo=None) + datetime.timedelta(hours=7)) and (datetime.datetime.now() >= ujian.waktu_mulai.replace(tzinfo=None) + datetime.timedelta(hours=7))):
                    # ujian masih valid
                    sweetify.info(request, 'Maaf, silahkan kerjakan ujian yang tersedia terlebih dahulu')
                    return HttpResponseRedirect(reverse('informasi_ujian'))
                else:
                    # Jika ujian sudah tidak valid
                    hasil_ujian = HasilUjian(user=request.user, ujian=ujian, waktu_mulai_mengerjakan=datetime.datetime.now())
                    hasil_ujian.save()

            # Periksa waktu ujian
            if (not ((datetime.datetime.now() <= ujian.waktu_selesai.replace(tzinfo=None) + datetime.timedelta(hours=7)) and (
                    datetime.datetime.now() >= ujian.waktu_mulai.replace(tzinfo=None) + datetime.timedelta(hours=7))) and not hasil_ujian.waktu_selesai_mengerjakan):
                # Jika waktu telah habis dan user menekan halaman hasil
                hasil_ujian.waktu_selesai_mengerjakan = datetime.datetime.now()
                hasil_ujian.save()

            if hasil_ujian.waktu_selesai_mengerjakan:
                # Ambil konfigurasi pdf
                konfigurasi_pdf = HasilUjianPDFConfig.objects.filter().last()
                print(konfigurasi_pdf.logo_kiri)

                # Create the HttpResponse object with the appropriate PDF headers.
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'filename="somefilename.pdf"'

                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response, pagesize=A4)
                p.setFont('Helvetica', 10)
                p.setLineWidth(1)
                # Garis header
                p.line(100, 750, 500, 750)
                # Header
                p.drawString(210, 800, 'PANITIA UJI KOMPETENSI/SELEKSI')
                p.drawString(170, 785, 'PENGISIAN PENGANGKATAN PERANGKAT DESA')
                p.drawString(210, 770, 'KABUPATEN SRAGEN TAHUN 2018')
                p.drawString(140, 755, 'FAKULTAS EKONOMIKA DAN BISNIS UNIVERSITAS DIPONEGORO')

                # Judul
                p.setFont('Helvetica', 12)
                p.drawString(230, 720, 'HASIL UJIAN TERTULIS')
                p.drawString(200, 700, 'COMPUTER ASSISTED TEST (CAT)')

                # Waktu cetak
                p.setFont('Helvetica', 8)
                p.drawString(260, 685, format_date(datetime.datetime.now(), format='full', locale='id'))

                # Data Peserta
                p.setFont('Helvetica', 12)
                p.drawString(60, 650, 'NAMA PESERTA     :')
                p.drawString(180, 650, request.user.profiluser.nama_peserta)
                p.drawString(60, 630, 'NOMOR PESERTA  :')
                p.drawString(180, 630, request.user.username)
                p.drawString(60, 610, 'KECAMATAN           :')
                p.drawString(180, 610, request.user.profiluser.kecamatan)
                p.drawString(60, 590, 'DESA                        :')
                p.drawString(180, 590, request.user.profiluser.desa)
                p.drawString(60, 570, 'FORMASI                 :')
                p.drawString(180, 570, request.user.profiluser.formasi)
                p.drawString(60, 550, 'NILAI                        :')

                # Nilai
                nilai = 0
                soal_ujian = SoalUjian.objects.filter(ujian=ujian)
                for soal in soal_ujian:
                    try:
                        jawaban_user = JawabanUser.objects.get(soal_ujian=soal, hasil_ujian=hasil_ujian)
                    except JawabanUser.DoesNotExist:
                        pass
                    else:
                        if soal.huruf_jawaban == jawaban_user.huruf_jawaban:
                            nilai += 1
                        else:
                            pass

                p.drawString(180, 550, str(nilai))
                p.showPage()
                p.save()
                return response
            else:
                sweetify.error(request, 'Maaf, waktu ujian masih berlangsung atau anda belum meyelesaikan ujian')
                return HttpResponseRedirect(reverse('informasi_ujian'))


        else:
            sweetify.error(request, 'Maaf, belum ada ujian yang tersedia')
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        sweetify.error(request, 'Metode request tidak valid')
        return HttpResponseRedirect(reverse('user_profile'))