from flask import flash, redirect, render_template, request, session, url_for
from models.db import get_db_connection
from engine.cf_engine import CertaintyFactorEngine
from engine.backward_engine import BackwardChainingEngine

class DiagnosaController:
    def mulaiKonsultasi(self):
        if 'penyakit_list' not in session:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY id")
            semua_penyakit = cursor.fetchall()
            cursor.execute("SELECT * FROM Aturan_Tabel")
            semua_aturan = cursor.fetchall()
            conn.close()
            session['penyakit_list'] = [dict(p) for p in semua_penyakit]
            session['aturan_list'] = [dict(a) for a in semua_aturan]
            session['gejala_jawab'] = {}
            session['penyakit_index'] = 0

        penyakit_list = session.get('penyakit_list', [])
        aturan_list = session.get('aturan_list', [])
        gejala_jawab = session.get('gejala_jawab', {})
        penyakit_index = session.get('penyakit_index', 0)

        if penyakit_index >= len(penyakit_list):
            return self.hitungHasilDiagnosa()

        penyakit = penyakit_list[penyakit_index]
        penyakit_id = penyakit['id']
        gejala_penyakit = [a for a in aturan_list if a['penyakit_id'] == penyakit_id]

        for aturan in gejala_penyakit:
            gejala_id = aturan['gejala_id']
            if str(gejala_id) not in gejala_jawab:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Gejala_Tabel WHERE id = %s", (gejala_id,))
                gejala = cursor.fetchone()
                conn.close()

                return render_template(
                    'user/konsultasi.html',
                    current_step='question',
                    gejala=gejala,
                    current_question=len(gejala_jawab) + 1
                )

        session['penyakit_index'] = penyakit_index + 1
        return self.mulaiKonsultasi()

    def prosesJawabanGejala(self, gejala_id, jawaban):
        gejala_jawab = session.get('gejala_jawab', {})
        gejala_jawab[str(gejala_id)] = float(jawaban)
        session['gejala_jawab'] = gejala_jawab
        return self.mulaiKonsultasi()

    def hitungHasilDiagnosa(self):
        gejala_jawab = session.get('gejala_jawab', {})
        penyakit_list = session.get('penyakit_list', [])
        aturan_list = session.get('aturan_list', [])

        cf_engine = CertaintyFactorEngine()
        penyakit_dict = {}

        for aturan in aturan_list:
            pid = aturan['penyakit_id']
            gid = str(aturan['gejala_id'])

            if pid not in penyakit_dict:
                penyakit = next((p for p in penyakit_list if p['id'] == pid), None)
                penyakit_dict[pid] = {
                    'nama_penyakit': penyakit['nama_penyakit'],
                    'deskripsi_penyakit': penyakit['deskripsi'],
                    'solusi_penyakit': penyakit['solusi'],
                    'cf_list': []
                }

            if gid in gejala_jawab:
                cf_user = gejala_jawab[gid]
                cf = cf_engine.hitung_cf(cf_user, aturan['mb'], aturan['md'])
                penyakit_dict[pid]['cf_list'].append(cf)

        hasil_diagnosa = []
        for pid, data in penyakit_dict.items():
            if data['cf_list']:
                nilai_cf = cf_engine.kombinasi_cf(data['cf_list'])
                hasil_diagnosa.append({
                    'penyakit_id': pid,
                    'nama_penyakit': data['nama_penyakit'],
                    'deskripsi_penyakit': data['deskripsi_penyakit'],
                    'solusi_penyakit': data['solusi_penyakit'],
                    'nilai_cf': round(nilai_cf, 2)
                })

        hasil_diagnosa.sort(key=lambda x: x['nilai_cf'], reverse=True)

        if hasil_diagnosa:
            conn = get_db_connection()
            if conn is None:
                flash('Gagal terhubung ke database.', 'danger')
                return redirect(url_for('konsultasi_route'))

            cursor = conn.cursor()
            cursor.execute("DELETE FROM HasilDiagnosa_Tabel WHERE user_id = %s", (session['user_id'],))

            penyakit_tertinggi = hasil_diagnosa[0]['penyakit_id']
            gejala_relevan = []
            for aturan in aturan_list:
                if aturan['penyakit_id'] == penyakit_tertinggi:
                    gejala_id = str(aturan['gejala_id'])
                    if gejala_id in gejala_jawab:
                        gejala_relevan.append(gejala_id)

            gejala_terpilih = ','.join(gejala_relevan)

            cursor.execute('''
                INSERT INTO HasilDiagnosa_Tabel (
                  user_id, penyakit_id, nilai_cf, tanggal_diagnosa, gejala_terpilih
                ) VALUES (%s, %s, %s, NOW(), %s)
            ''', (
                session['user_id'],
                hasil_diagnosa[0]['penyakit_id'],
                hasil_diagnosa[0]['nilai_cf'],
                gejala_terpilih
            ))

            conn.commit()
            conn.close()

        for key in ['penyakit_list', 'aturan_list', 'gejala_jawab', 'penyakit_index']:
            session.pop(key, None)

        return render_template(
            'user/konsultasi.html',
            current_step='result',
            hasil=hasil_diagnosa[0] if hasil_diagnosa else None
        )