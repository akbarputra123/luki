from flask import flash, redirect, render_template, url_for
from models.db import get_db_connection

class RiwayatController:
    def lihatRiwayatDiagnosa(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT h.id, h.tanggal_diagnosa, h.nilai_cf, 
                   u.username, 
                   p.nama_penyakit,
                   (
                       SELECT GROUP_CONCAT(g.nama_gejala SEPARATOR ', ')
                       FROM Gejala_Tabel g
                       WHERE FIND_IN_SET(g.id, h.gejala_terpilih)
                   ) AS gejala
            FROM HasilDiagnosa_Tabel h
            JOIN User_Tabel u ON h.user_id = u.id
            JOIN Penyakit_Tabel p ON h.penyakit_id = p.id
            ORDER BY h.tanggal_diagnosa DESC
        ''')
        daftar_riwayat = cursor.fetchall()

        # Ubah string gejala menjadi list
        for r in daftar_riwayat:
            if r['gejala']:
                r['gejala'] = [g.strip() for g in r['gejala'].split(',')]
            else:
                r['gejala'] = []

        conn.close()
        return render_template('admin/riwayat.html', daftar_riwayat=daftar_riwayat)

    def lihatDetailDiagnosa(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ambil data diagnosa berdasarkan ID, termasuk username
        cursor.execute('''
            SELECT h.id, h.tanggal_diagnosa, h.nilai_cf, h.gejala_terpilih,
                   u.username, 
                   p.id AS penyakit_id, p.kode_penyakit, p.nama_penyakit, p.deskripsi, p.solusi
            FROM HasilDiagnosa_Tabel h
            JOIN User_Tabel u ON h.user_id = u.id
            JOIN Penyakit_Tabel p ON h.penyakit_id = p.id
            WHERE h.id = %s
        ''', (id,))
        diagnosa = cursor.fetchone()
        
        if not diagnosa:
            flash('Data diagnosa tidak ditemukan', 'error')
            return redirect(url_for('riwayat_route'))

        gejala_list = []
        if diagnosa['gejala_terpilih']:
            gejala_ids = diagnosa['gejala_terpilih'].split(',')
            format_strings = ','.join(['%s'] * len(gejala_ids))
            cursor.execute(f'''
                SELECT kode_gejala, nama_gejala
                FROM Gejala_Tabel
                WHERE id IN ({format_strings})
            ''', gejala_ids)
            gejala_list = cursor.fetchall()

        conn.close()
        
        return render_template('admin/riwayat.html', 
                               diagnosa=diagnosa,
                               gejala_list=gejala_list)
