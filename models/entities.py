# models/entities.py
from abc import ABC, abstractmethod
from flask import session
from models.db import get_db_connection
import bcrypt
from datetime import datetime
from models.objects import Gejala, Penyakit, Aturan, HasilDiagnosa

# Abstract class Akun
class Akun(ABC):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @abstractmethod
    def login(self):
        pass

# User class
class User(Akun):
    def __init__(self, id, username, password, nama_lengkap, tanggal_lahir):
        super().__init__(id, username, password)
        self.nama_lengkap = nama_lengkap
        self.tanggal_lahir = tanggal_lahir

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
        from models.managers import AturanManager, PenyakitManager
        aturan_mgr = AturanManager()
        penyakit_mgr = PenyakitManager()
        cf_engine = CertaintyFactorEngine()

        aturan_list = aturan_mgr.lihatSemuaAturan()
        penyakit_list = penyakit_mgr.lihatSemuaPenyakit()

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

        conn = get_db_connection()
        cursor = conn.cursor()
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
    

# Admin class
class Admin(Akun):
    def __init__(self, id, username, password):
        super().__init__(id, username, password)

    def kelolaGejala(self):
        from models.managers import GejalaManager
        return GejalaManager().lihatSemuaGejala()

    def kelolaPenyakit(self):
        from models.managers import PenyakitManager
        return PenyakitManager().lihatSemuaPenyakit()

    def kelolaAturan(self):
        from models.managers import AturanManager
        return AturanManager().lihatSemuaAturan()

    def lihatRiwayat(self):
        from models.managers import RiwayatManager
        return RiwayatManager().lihatSemuaRiwayat()


# Certainty Factor Engine
class CertaintyFactorEngine:
    def hitungCF(self, mb, md):
        return mb - md

    def kombinasiCF(self, cf_list):
        if not cf_list:
            return 0
        combined = cf_list[0]
        for cf in cf_list[1:]:
            combined = combined + cf * (1 - combined)
        return combined

# Backward Chaining Engine (opsional)
class BackwardChainingEngine:
    def inferensi(self, user_input):
        pass  # Belum diimplementasikan
