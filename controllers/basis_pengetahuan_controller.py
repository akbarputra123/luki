from flask import render_template  # ✅ WAJIB untuk render_template berfungsi
from models.db import get_db_connection

class BasisPengetahuanController:
    def lihatSemuaGejala(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
        daftar_gejala = cursor.fetchall()
        conn.close()
        return daftar_gejala
    
    def lihatSemuaPenyakit(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        daftar_penyakit = cursor.fetchall()
        conn.close()
        return daftar_penyakit
    
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
    
    def lihatBasisPengetahuan(self):
        daftar_gejala = self.lihatSemuaGejala()
        daftar_penyakit = self.lihatSemuaPenyakit()
        daftar_aturan = self.lihatSemuaAturan()
        
        return render_template('admin/basis.html',
                            daftar_gejala=daftar_gejala,
                            daftar_penyakit=daftar_penyakit,
                            daftar_aturan=daftar_aturan)
    
    def lihatGejala(self):
        daftar_gejala = self.lihatSemuaGejala()
        return render_template('admin/card_gejala.html',
                            daftar_gejala=daftar_gejala)
    
    def lihatPenyakit(self):
        daftar_penyakit = self.lihatSemuaPenyakit()
        return render_template('admin/card_penyakit.html',
                            daftar_penyakit=daftar_penyakit)
    
    def lihatAturan(self):
        daftar_aturan = self.lihatSemuaAturan()
        return render_template('admin/card_aturan.html',
                            daftar_aturan=daftar_aturan)
    