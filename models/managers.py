from models.objects import Gejala, Penyakit, Aturan, HasilDiagnosa
from models.db import get_db_connection

class GejalaManager:
    def lihatSemuaGejala(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
        gejala_list = [Gejala(**g) for g in cursor.fetchall()]
        conn.close()
        return gejala_list

class PenyakitManager:
    def lihatSemuaPenyakit(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        penyakit_list = [Penyakit(**p) for p in cursor.fetchall()]
        conn.close()
        return penyakit_list

class AturanManager:
    def lihatSemuaAturan(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT a.id, a.penyakit_id, a.gejala_id, a.mb, a.md FROM Aturan_Tabel a ORDER BY a.id")
        aturan_list = [Aturan(**a) for a in cursor.fetchall()]
        conn.close()
        return aturan_list

class RiwayatManager:
    def lihatSemuaRiwayat(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM HasilDiagnosa_Tabel ORDER BY tanggal_diagnosa DESC")
        riwayat_list = [HasilDiagnosa(**h) for h in cursor.fetchall()]
        conn.close()
        return riwayat_list

class DiagnosaEngine:
    def prosesKonsultasi(self):
        from models.entities import CertaintyFactorEngine
        cf_engine = CertaintyFactorEngine()
        # Implementasi akan ditambahkan di sini
        pass
