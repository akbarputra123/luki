from flask import flash, redirect, render_template, request, url_for
from models.db import get_db_connection

class ManajemenAturanController:
    def lihatDaftarAturan(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.mb, a.md, 
                   p.id as penyakit_id, p.kode_penyakit, p.nama_penyakit,
                   g.id as gejala_id, g.kode_gejala, g.nama_gejala
            FROM Aturan_Tabel a
            JOIN Penyakit_Tabel p ON a.penyakit_id = p.id
            JOIN Gejala_Tabel g ON a.gejala_id = g.id
            ORDER BY p.kode_penyakit, g.kode_gejala
        ''')
        daftar_aturan = cursor.fetchall()
        
        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        daftar_penyakit = cursor.fetchall()
        
        cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
        daftar_gejala = cursor.fetchall()
        
        conn.close()
        
        return render_template('admin/aturan.html', 
                            daftar_aturan=daftar_aturan,
                            daftar_penyakit=daftar_penyakit,
                            daftar_gejala=daftar_gejala)

    def tambahAturan(self):
        if request.method == 'POST':
            penyakit_id = request.form['penyakit_id']
            gejala_id = request.form['gejala_id']
            mb = float(request.form['mb'])
            md = float(request.form['md'])

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    SELECT * FROM Aturan_Tabel 
                    WHERE penyakit_id = %s AND gejala_id = %s
                ''', (penyakit_id, gejala_id))
                existing = cursor.fetchone()
                
                if existing:
                    flash('Aturan untuk penyakit dan gejala ini sudah ada', 'error')
                else:
                    cursor.execute('''
                        INSERT INTO Aturan_Tabel (penyakit_id, gejala_id, mb, md)
                        VALUES (%s, %s, %s, %s)
                    ''', (penyakit_id, gejala_id, mb, md))
                    conn.commit()
                    flash('Aturan berhasil ditambahkan', 'success')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
            finally:
                conn.close()
            
        return redirect(url_for('aturan_route'))

    def editAturan(self, id):
        if request.method == 'POST':
            mb = float(request.form['mb'])
            md = float(request.form['md'])
            penyakit_id = request.form['penyakit_id']
            gejala_id = request.form['gejala_id']

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Cek duplikasi jika kombinasi penyakit dan gejala baru sudah ada
                cursor.execute('''
                    SELECT * FROM Aturan_Tabel 
                    WHERE penyakit_id = %s AND gejala_id = %s AND id != %s
                ''', (penyakit_id, gejala_id, id))
                existing = cursor.fetchone()

                if existing:
                    flash('Aturan dengan kombinasi penyakit dan gejala ini sudah ada', 'error')
                else:
                    cursor.execute('''
                        UPDATE Aturan_Tabel 
                        SET penyakit_id=%s, gejala_id=%s, mb=%s, md=%s 
                        WHERE id=%s
                    ''', (penyakit_id, gejala_id, mb, md, id))
                    conn.commit()
                    flash('Aturan berhasil diperbarui', 'success')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
            finally:
                conn.close()

            return redirect(url_for('aturan_route'))

        # GET: Tampilkan form edit manual jika diperlukan
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.mb, a.md, 
                   p.id as penyakit_id, p.kode_penyakit, p.nama_penyakit,
                   g.id as gejala_id, g.kode_gejala, g.nama_gejala
            FROM Aturan_Tabel a
            JOIN Penyakit_Tabel p ON a.penyakit_id = p.id
            JOIN Gejala_Tabel g ON a.gejala_id = g.id
            WHERE a.id = %s
        ''', (id,))
        aturan = cursor.fetchone()

        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        daftar_penyakit = cursor.fetchall()

        cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
        daftar_gejala = cursor.fetchall()

        conn.close()

        if not aturan:
            flash('Aturan tidak ditemukan', 'error')
            return redirect(url_for('aturan_route'))

        return render_template('admin/edit_aturan.html', 
                            aturan=aturan,
                            daftar_penyakit=daftar_penyakit,
                            daftar_gejala=daftar_gejala)

    def hapusAturan(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Aturan_Tabel WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        flash('Aturan berhasil dihapus', 'success')
        return redirect(url_for('aturan_route'))
