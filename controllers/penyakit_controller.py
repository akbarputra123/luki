from flask import flash, redirect, render_template, request, url_for
from models.db import get_db_connection
import pymysql

class ManajemenPenyakitController:
    def lihatDaftarPenyakitHama(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
        daftar_penyakit = cursor.fetchall()
        conn.close()
        return render_template('admin/hama.html', daftar_penyakit=daftar_penyakit)
    
    def tambahPenyakitHama(self):
        if request.method == 'POST':
            kode_penyakit = request.form['kode_penyakit']
            nama_penyakit = request.form['nama_penyakit']
            deskripsi = request.form['deskripsi']
            solusi = request.form['solusi']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Penyakit_Tabel (kode_penyakit, nama_penyakit, deskripsi, solusi) VALUES (%s, %s, %s, %s)",
                    (kode_penyakit, nama_penyakit, deskripsi, solusi)
                )
                conn.commit()
                flash('Penyakit/Hama berhasil ditambahkan', 'success')
            except pymysql.IntegrityError:
                flash('Kode penyakit/hama sudah ada', 'error')
            finally:
                conn.close()
            
        return redirect(url_for('hama_route'))
    
    def editPenyakitHama(self, id):
        if request.method == 'POST':
            kode_penyakit = request.form['kode_penyakit']
            nama_penyakit = request.form['nama_penyakit']
            deskripsi = request.form['deskripsi']
            solusi = request.form['solusi']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE Penyakit_Tabel SET kode_penyakit=%s, nama_penyakit=%s, deskripsi=%s, solusi=%s WHERE id=%s",
                    (kode_penyakit, nama_penyakit, deskripsi, solusi, id)
                )
                conn.commit()
                flash('Penyakit/Hama berhasil diperbarui', 'success')
            except pymysql.IntegrityError:
                flash('Kode penyakit/hama sudah ada', 'error')
            finally:
                conn.close()
            
            return redirect(url_for('hama_route'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Penyakit_Tabel WHERE id = %s", (id,))
        penyakit = cursor.fetchone()
        conn.close()
        
        if not penyakit:
            flash('Penyakit/Hama tidak ditemukan', 'error')
            return redirect(url_for('hama_route'))
            
        return render_template('admin/edit_hama.html', penyakit=penyakit)
    
    def hapusPenyakitHama(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Penyakit_Tabel WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        flash('Penyakit/Hama berhasil dihapus', 'success')
        return redirect(url_for('hama_route'))
    