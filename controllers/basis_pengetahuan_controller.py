from models.db import get_db_connection

class BasisPengetahuanController:
    # Fungsi untuk mengambil semua gejala dari database
    def lihatSemuaGejala(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
        daftar_gejala = cursor.fetchall()
        conn.close()
        return daftar_gejala

    # Fungsi untuk mengambil semua penyakit dari database
    def lihatSemuaPenyakit(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        daftar_penyakit = cursor.fetchall()
        conn.close()
        return daftar_penyakit

    # Fungsi untuk mengambil semua aturan dari database
    def lihatSemuaAturan(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.mb, a.md, 
                   p.kode_penyakit, p.nama_penyakit,
                   g.kode_gejala, g.nama_gejala
            FROM Aturan_Tabel a
            JOIN Penyakit_Tabel p ON a.penyakit_id = p.id
            JOIN Gejala_Tabel g ON a.gejala_id = g.id
            ORDER BY p.kode_penyakit, g.kode_gejala
        ''')
        daftar_aturan = cursor.fetchall()
        conn.close()
        return daftar_aturan
