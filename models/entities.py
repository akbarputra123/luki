from abc import ABC, abstractmethod
from flask import session
from models.db import get_db_connection
from datetime import datetime
import bcrypt

from models.objects import Gejala, Penyakit, Aturan, HasilDiagnosa

# Abstract class Akun
class Akun(ABC):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @abstractmethod
    def login(self, username, password):
        pass

# ==========================
# USER CLASS
# ==========================
class User(Akun):
    def __init__(self, id, username, password, namaLengkap, tanggalLahir):
        super().__init__(id, username, password)
        self.nama_lengkap = namaLengkap
        self.tanggal_lahir = tanggalLahir

    def login(self, username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User_Tabel WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return User(user['id'], user['username'], user['password'], user['nama_lengkap'], user['tanggal_lahir'])
        return None

    def register(self, nama, username, password, confirm_password, tanggal_lahir):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User_Tabel WHERE username = %s', (username,))
        if cursor.fetchone():
            return False, 'Username sudah digunakan'

        if password != confirm_password:
            return False, 'Konfirmasi password tidak cocok'

        hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO User_Tabel (username, password, role, nama_lengkap, tanggal_lahir)
            VALUES (%s, %s, %s, %s, %s)
        ''', (username, hash_pw.decode('utf-8'), 'user', nama, tanggal_lahir))
        conn.commit()
        conn.close()
        return True, 'Registrasi berhasil'

    def lupaPassword(self, username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User_Tabel WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        if not user:
            return False, 'Username tidak ditemukan'
        session['reset_user'] = username
        return True, 'Username valid'

    def verifikasiTanggalLahir(self, tanggal_lahir):
        username = session.get('reset_user')
        if not username:
            return False, 'Sesi tidak valid'
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User_Tabel WHERE username = %s AND tanggal_lahir = %s",
                       (username, tanggal_lahir))
        user = cursor.fetchone()
        conn.close()
        if not user:
            return False, 'Tanggal lahir tidak sesuai'
        return True, 'Verifikasi berhasil'

    def ubahPasswordBaru(self, new_password, confirm_password):
        if new_password != confirm_password:
            return False, 'Konfirmasi password salah'
        username = session.get('reset_user')
        if not username:
            return False, 'Sesi tidak valid'
        hash_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE User_Tabel SET password = %s WHERE username = %s",
                       (hash_pw.decode('utf-8'), username))
        conn.commit()
        conn.close()
        return True, 'Password berhasil diperbarui'

    def konsultasi(self, gejala_terpilih_ids):
        cf_engine = CertaintyFactorEngine()

        # Ambil semua aturan
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aturan_Tabel")
        aturan_list = [Aturan(**a) for a in cursor.fetchall()]

        # Ambil semua penyakit
        cursor.execute("SELECT * FROM Penyakit_Tabel")
        penyakit_list = [Penyakit(**p) for p in cursor.fetchall()]

        hasil_cf = {}
        for penyakit in penyakit_list:
            cf_values = []
            for aturan in aturan_list:
                if aturan.penyakit_id == penyakit.id and str(aturan.gejala_id) in gejala_terpilih_ids:
                    cf = cf_engine.hitungCF(aturan.mb, aturan.md)
                    cf_values.append(cf)
            combined_cf = cf_engine.kombinasiCF(cf_values)
            if combined_cf > 0:
                hasil_cf[penyakit.id] = combined_cf

        if not hasil_cf:
            return False, 'Tidak ada diagnosa yang cocok'

        penyakit_tertinggi = max(hasil_cf, key=hasil_cf.get)
        nilai_cf_tertinggi = hasil_cf[penyakit_tertinggi]

        cursor.execute('''
            INSERT INTO HasilDiagnosa_Tabel (user_id, penyakit_id, nilai_cf, tanggal_diagnosa, gejala_terpilih)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            self.id, penyakit_tertinggi, nilai_cf_tertinggi,
            datetime.now(), ','.join(gejala_terpilih_ids)
        ))
        conn.commit()
        conn.close()

        return True, 'Diagnosa berhasil disimpan'

    def lihatHasil(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM HasilDiagnosa_Tabel 
            WHERE user_id = %s ORDER BY tanggal_diagnosa DESC
        ''', (self.id,))
        hasil_list = [HasilDiagnosa(**row) for row in cursor.fetchall()]
        conn.close()
        return hasil_list

# ==========================
# ADMIN CLASS
# ==========================
class Admin(Akun):
    def __init__(self, id, username, password):
        super().__init__(id, username, password)

    def kelolaGejala(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
        gejala_list = [Gejala(**g) for g in cursor.fetchall()]
        conn.close()
        return gejala_list

    def kelolaPenyakit(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        penyakit_list = [Penyakit(**p) for p in cursor.fetchall()]
        conn.close()
        return penyakit_list

    def kelolaAturan(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aturan_Tabel ORDER BY id")
        aturan_list = [Aturan(**a) for a in cursor.fetchall()]
        conn.close()
        return aturan_list

    def lihatRiwayat(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM HasilDiagnosa_Tabel ORDER BY tanggal_diagnosa DESC")
        riwayat_list = [HasilDiagnosa(**r) for r in cursor.fetchall()]
        conn.close()
        return riwayat_list

# ==========================
# CERTAINTY FACTOR ENGINE
# ==========================
class CertaintyFactorEngine:
    def hitungCF(self, mb, md):
        return mb - md

    def kombinasiCF(self, cf_list):
        if not cf_list:
            return 0
        combined = cf_list[0]
        for cf in cf_list[1:]:
            combined = combined + cf * (1 - combined)
        return round(combined, 4)

# ==========================
# BACKWARD CHAINING ENGINE (opsional)
# ==========================
class BackwardChainingEngine:
    def inferensi(self, gejala_terpilih_ids):
        # Contoh implementasi dasar untuk backward chaining
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ambil semua aturan
        cursor.execute("SELECT * FROM Aturan_Tabel")
        aturan_list = cursor.fetchall()

        # Ambil semua penyakit
        cursor.execute("SELECT * FROM Penyakit_Tabel")
        penyakit_list = cursor.fetchall()

        hasil = []
        for penyakit in penyakit_list:
            id_penyakit = penyakit['id']
            gejala_penyakit = [a['gejala_id'] for a in aturan_list if a['penyakit_id'] == id_penyakit]
            if all(str(gid) in gejala_terpilih_ids for gid in gejala_penyakit):
                hasil.append(penyakit)

        conn.close()
        return hasil if hasil else None
