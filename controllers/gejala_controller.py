from flask import flash, redirect, render_template, request, url_for
from models.db import get_db_connection
import pymysql
from pymysql.err import IntegrityError  # gunakan dari pymysql, bukan mysql.connector

class ManajemenGejalaController:
    def lihatDaftarGejala(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Gejala_Tabel ORDER BY kode_gejala")
            daftar_gejala = cursor.fetchall()

            # Ambil kode terakhir dari kolom kode_gejala
            cursor.execute("SELECT kode_gejala FROM Gejala_Tabel ORDER BY id DESC LIMIT 1")
            hasil_kode = cursor.fetchone()

            if hasil_kode:
                kode_terakhir = hasil_kode['kode_gejala']
            else:
                kode_terakhir = 'G01'

            conn.close()
            return render_template('admin/gejala.html', daftar_gejala=daftar_gejala, kode_terakhir=kode_terakhir)

        except Exception as e:
             flash(f"Terjadi error saat memuat data: {e}", 'danger')
        return render_template('admin/gejala.html', daftar_gejala=[], kode_terakhir='G01')


    def editGejala(self, id):
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

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
            except IntegrityError as e:
                if e.args[0] == 1062:  # Duplicate entry
                    flash('Kode gejala sudah ada.', 'danger')
                else:
                    flash(f'Error saat memperbarui data: {str(e)}', 'danger')
            finally:
                conn.close()

            return redirect(url_for('gejala_route'))

        # GET request untuk form edit
        cursor.execute("SELECT * FROM Gejala_Tabel WHERE id = %s", (id,))
        gejala = cursor.fetchone()
        conn.close()

        if not gejala:
            flash('Gejala tidak ditemukan', 'danger')
            return redirect(url_for('gejala_route'))

        return render_template('admin/edit_gejala.html', gejala=gejala)

    def hapusGejala(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Gejala_Tabel WHERE id = %s", (id,))
            conn.commit()
            flash('Gejala berhasil dihapus', 'success')
        except IntegrityError as e:
            if e.args[0] == 1451:  # Foreign key constraint
                flash('Gejala tidak dapat dihapus karena sedang digunakan di data aturan.', 'danger')
            else:
                flash(f'Error saat menghapus data: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('gejala_route'))
