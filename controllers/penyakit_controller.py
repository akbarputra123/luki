from flask import flash, redirect, render_template, request, url_for
from models.db import get_db_connection
import pymysql
from pymysql.err import IntegrityError

class ManajemenPenyakitController:
    def lihatDaftarPenyakitHama(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Ambil semua data penyakit
            cursor.execute("SELECT * FROM Penyakit_Tabel ORDER BY kode_penyakit")
            daftar_penyakit = cursor.fetchall()

            # Ambil kode terakhir
            cursor.execute("SELECT kode_penyakit FROM Penyakit_Tabel ORDER BY id DESC LIMIT 1")
            hasil_kode = cursor.fetchone()
            kode_terakhir = hasil_kode['kode_penyakit'] if hasil_kode else 'P01'

            conn.close()
            return render_template('admin/hama.html', daftar_penyakit=daftar_penyakit, kode_terakhir=kode_terakhir)

        except Exception as e:
            flash(f"Terjadi error saat memuat data: {e}", 'danger')
        return render_template('admin/hama.html', daftar_penyakit=[], kode_terakhir='P01')

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
            except IntegrityError as e:
                if e.args[0] == 1062:  # Duplicate entry
                    flash('Kode penyakit/hama sudah ada.', 'danger')
                else:
                    flash(f'Terjadi error saat menambahkan data: {str(e)}', 'danger')
            finally:
                conn.close()

        return redirect(url_for('hama_route'))

    def editPenyakitHama(self, id):
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if request.method == 'POST':
            kode_penyakit = request.form['kode_penyakit']
            nama_penyakit = request.form['nama_penyakit']
            deskripsi = request.form['deskripsi']
            solusi = request.form['solusi']

            try:
                cursor.execute(
                    "UPDATE Penyakit_Tabel SET kode_penyakit=%s, nama_penyakit=%s, deskripsi=%s, solusi=%s WHERE id=%s",
                    (kode_penyakit, nama_penyakit, deskripsi, solusi, id)
                )
                conn.commit()
                flash('Penyakit/Hama berhasil diperbarui', 'success')
            except IntegrityError as e:
                if e.args[0] == 1062:  # Duplicate entry
                    flash('Kode penyakit/hama sudah ada.', 'danger')
                else:
                    flash(f'Terjadi error saat memperbarui data: {str(e)}', 'danger')
            finally:
                conn.close()

            return redirect(url_for('hama_route'))

        # GET request untuk menampilkan data pada form edit
        cursor.execute("SELECT * FROM Penyakit_Tabel WHERE id = %s", (id,))
        penyakit = cursor.fetchone()
        conn.close()

        if not penyakit:
            flash('Penyakit/Hama tidak ditemukan', 'danger')
            return redirect(url_for('hama_route'))

        return render_template('admin/edit_hama.html', penyakit=penyakit)

    def hapusPenyakitHama(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Penyakit_Tabel WHERE id = %s", (id,))
            conn.commit()
            flash('Penyakit/Hama berhasil dihapus', 'success')
        except IntegrityError as e:
            if e.args[0] == 1451:  # Foreign key constraint error
                flash('Penyakit/Hama tidak dapat dihapus karena masih digunakan di data aturan.', 'danger')
            else:
                flash(f'Gagal menghapus: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('hama_route'))
