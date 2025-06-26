from flask import flash, redirect, render_template, request, url_for
from models.db import get_db_connection
import pymysql


class ManajemenGejalaController:
    def lihatDaftarGejala(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
            daftar_gejala = cursor.fetchall()
            conn.close()
            return render_template('admin/gejala.html', daftar_gejala=daftar_gejala)
        except Exception as e:
            return f"Terjadi error: {e}"

    def tambahGejala(self):
        if request.method == 'POST':
            kode_gejala = request.form['kode_gejala']
            nama_gejala = request.form['nama_gejala']
            deskripsi = request.form['deskripsi']
            kategori = request.form['kategori']

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Gejala_Tabel (kode_gejala, nama_gejala, deskripsi, kategori) VALUES (%s, %s, %s, %s)",
                    (kode_gejala, nama_gejala, deskripsi, kategori)
                )
                conn.commit()
                flash('Gejala berhasil ditambahkan', 'success')
            except pymysql.IntegrityError:
                flash('Kode gejala sudah ada', 'error')
            finally:
                conn.close()
            
        return redirect(url_for('gejala_route'))

    def editGejala(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == 'POST':
            kode_gejala = request.form['kode_gejala']
            nama_gejala = request.form['nama_gejala']
            deskripsi = request.form['deskripsi']
            kategori = request.form['kategori']
            
            try:
                cursor.execute(
                    "UPDATE Gejala_Tabel SET kode_gejala=%s, nama_gejala=%s, deskripsi=%s, kategori=%s WHERE id=%s",
                    (kode_gejala, nama_gejala, deskripsi, kategori, id)
                )
                conn.commit()
                flash('Gejala berhasil diperbarui', 'success')
            except pymysql.IntegrityError:
                flash('Kode gejala sudah ada', 'error')
            finally:
                conn.close()
            
            return redirect(url_for('gejala_route'))

        cursor.execute("SELECT * FROM Gejala_Tabel WHERE id = %s", (id,))
        gejala = cursor.fetchone()
        conn.close()

        if not gejala:
            flash('Gejala tidak ditemukan', 'error')
            return redirect(url_for('gejala_route'))

        return render_template('admin/edit_gejala.html', gejala=gejala)

    def hapusGejala(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Gejala_Tabel WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        flash('Gejala berhasil dihapus', 'success')
        return redirect(url_for('gejala_route'))