from flask import Flask, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController
from controllers.gejala_controller import ManajemenGejalaController
from controllers.penyakit_controller import ManajemenPenyakitController
from controllers.aturan_controller import ManajemenAturanController
from controllers.riwayat_controller import RiwayatController
from controllers.basis_pengetahuan_controller import BasisPengetahuanController
from controllers.diagnosa_controller import DiagnosaController

app = Flask(__name__)
app.secret_key = 'secretkey'

# Initialize controllers
auth = AuthController()
gejala_controller = ManajemenGejalaController()
penyakit_controller = ManajemenPenyakitController()
aturan_controller = ManajemenAturanController()
riwayat_controller = RiwayatController()
basis_pengetahuan_controller = BasisPengetahuanController()
diagnosa_controller = DiagnosaController()

# Routes
@app.route('/', methods=['GET', 'POST'])
def login_route():
    return auth.login()

@app.route('/logout')
def logout_route():
    return auth.logout()

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return auth.register()

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password_route():
    return auth.lupaPassword()

@app.route('/verify-birthdate', methods=['GET', 'POST'])
def verifikasi_tanggal_route():
    return auth.verifikasiTanggalLahir()

@app.route('/reset-password', methods=['GET', 'POST'])
def ubah_password_route():
    return auth.ubahPasswordBaru()

@app.route('/dashboard_user')
def dashboard_user():
    return render_template('user/dashboard.html')

@app.route('/admin/dashboard')
def dashboard_admin():
    return render_template('admin/dashboard.html')


# Gejala Routes
@app.route('/admin/gejala', methods=['GET'])
def gejala_route():
    return gejala_controller.lihatDaftarGejala()

@app.route('/admin/gejala/tambah', methods=['POST'])
def tambah_gejala_route():
    return gejala_controller.tambahGejala()

@app.route('/admin/gejala/edit/<int:id>', methods=['GET', 'POST'])
def edit_gejala_route(id):
    return gejala_controller.editGejala(id)

@app.route('/admin/gejala/hapus/<int:id>', methods=['POST'])
def hapus_gejala_route(id):
    return gejala_controller.hapusGejala(id)

# Penyakit Routes
@app.route('/admin/hama', methods=['GET'])
def hama_route():
    return penyakit_controller.lihatDaftarPenyakitHama()

@app.route('/admin/hama/tambah', methods=['POST'])
def tambah_hama_route():
    return penyakit_controller.tambahPenyakitHama()

@app.route('/admin/hama/edit/<int:id>', methods=['GET', 'POST'])
def edit_hama_route(id):
    return penyakit_controller.editPenyakitHama(id)

@app.route('/admin/hama/hapus/<int:id>', methods=['POST'])
def hapus_hama_route(id):
    return penyakit_controller.hapusPenyakitHama(id)

# Aturan Routes
@app.route('/admin/aturan', methods=['GET'])
def aturan_route():
    return aturan_controller.lihatDaftarAturan()

@app.route('/admin/aturan/tambah', methods=['POST'])
def tambah_aturan_route():
    return aturan_controller.tambahAturan()

@app.route('/admin/aturan/edit/<int:id>', methods=['GET', 'POST'])
def edit_aturan_route(id):
    return aturan_controller.editAturan(id)

@app.route('/admin/aturan/hapus/<int:id>', methods=['POST'])
def hapus_aturan_route(id):
    return aturan_controller.hapusAturan(id)

# Riwayat Routes
@app.route('/admin/riwayat', methods=['GET'])
def riwayat_route():
    return riwayat_controller.lihatRiwayatDiagnosa()

@app.route('/admin/riwayat/detail/<int:id>', methods=['GET'])
def detail_riwayat_route(id):
    return riwayat_controller.lihatDetailDiagnosa(id)

# Diagnosa Routes
@app.route('/konsultasi', methods=['GET', 'POST'])
def konsultasi_route():
    if 'user_id' not in session:
        return redirect(url_for('login_route'))  # atau sesuai login kamu

    from controllers.diagnosa_controller import DiagnosaController
    diagnosa_controller = DiagnosaController()

    if request.method == 'POST':
        if 'mulai' in request.form:
            return diagnosa_controller.mulaiKonsultasi()
        elif 'jawaban_step' in request.form:
            return diagnosa_controller.prosesJawabanGejala(
                request.form['gejala_id'],
                request.form['jawaban']
            )

    return render_template('user/konsultasi.html', current_step='start')


@app.route('/riwayat-konsultasi')
def riwayat_konsultasi_route():
    if 'user_id' not in session:
        return redirect(url_for('login_route'))
    return riwayat_controller.lihatRiwayatDiagnosa()

@app.route('/riwayat-konsultasi/detail/<int:id>')
def detail_riwayat_konsultasi_route(id):
    if 'user_id' not in session:
        return redirect(url_for('login_route'))
    return diagnosa_controller.lihatDetailRiwayat(id)
# Add these new routes to your Flask app

# Basis Pengetahuan Route
@app.route('/admin/basis-pengetahuan', methods=['GET'])
def basis_pengetahuan_route():
    daftar_gejala = basis_pengetahuan_controller.lihatSemuaGejala()
    daftar_penyakit = basis_pengetahuan_controller.lihatSemuaPenyakit()
    daftar_aturan = basis_pengetahuan_controller.lihatSemuaAturan()
    return render_template('admin/basis.html',
                           daftar_gejala=daftar_gejala,
                           daftar_penyakit=daftar_penyakit,
                           daftar_aturan=daftar_aturan)


@app.route('/admin/basis-pengetahuan/gejala')
def card_gejala_route():
    daftar_gejala = basis_pengetahuan_controller.lihatSemuaGejala()
    return render_template('admin/card_gejala.html',
                           daftar_gejala=daftar_gejala)

@app.route('/admin/basis-pengetahuan/penyakit')
def card_penyakit_route():
    daftar_penyakit = basis_pengetahuan_controller.lihatSemuaPenyakit()
    return render_template('admin/card_penyakit.html',
                           daftar_penyakit=daftar_penyakit)

@app.route('/admin/basis-pengetahuan/aturan')
def card_aturan_route():
    daftar_aturan = basis_pengetahuan_controller.lihatSemuaAturan()
    return render_template('admin/card_aturan.html',
                           daftar_aturan=daftar_aturan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
