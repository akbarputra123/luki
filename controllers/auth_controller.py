from flask import flash, redirect, render_template, request, session, url_for
from models.db import get_db_connection
import bcrypt

class AuthController:
    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password_input = request.form['password'].encode('utf-8')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Tabel WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()

            if user:
                if user['role'] == 'admin':
                    if password_input.decode('utf-8') == user['password']:
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        session['role'] = user['role']
                        return redirect(url_for('dashboard_admin'))
                    else:
                        flash('Password salah untuk admin.', 'error')
                else:
                    if bcrypt.checkpw(password_input, user['password'].encode('utf-8')):
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        session['role'] = user['role']
                        return redirect(url_for('dashboard_user'))
                    else:
                        flash("Password salah.", 'error')
            else:
                flash("Username tidak ditemukan.", 'error')

        return render_template("auth/login.html")

    def logout(self):
        session.clear()
        return redirect(url_for('login_route'))

    def register(self):
        if request.method == 'POST':
            nama = request.form['nama_lengkap']
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm_password']
            tanggal_lahir = request.form['tanggal_lahir']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM User_Tabel WHERE username = %s', (username,))
            akun = cursor.fetchone()

            if akun:
                flash('Username sudah digunakan.')
            elif password != confirm:
                flash('Konfirmasi password tidak cocok.')
            else:
                hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('''
                    INSERT INTO User_Tabel (username, password, role, nama_lengkap, tanggal_lahir)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (username, hash_pw.decode('utf-8'), 'user', nama, tanggal_lahir))
                conn.commit()
                flash('Registrasi berhasil. Silakan login.')
                conn.close()
                return redirect(url_for('login_route'))

            conn.close()

        return render_template('auth/register.html')

    def lupaPassword(self):
        if request.method == 'POST':
            username = request.form['username']
            session['reset_user'] = username
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Tabel WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return redirect(url_for('verifikasi_tanggal_route'))
            else:
                flash('Username tidak ditemukan.')
        return render_template('auth/forgot.html')

    def verifikasiTanggalLahir(self):
        if request.method == 'POST':
            tanggal = request.form['tanggal_lahir']
            username = session.get('reset_user')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Tabel WHERE username = %s AND tanggal_lahir = %s", (username, tanggal))
            user = cursor.fetchone()
            conn.close()
            if user:
                return redirect(url_for('ubah_password_route'))
            else:
                flash('Verifikasi gagal.')
        return render_template('auth/tanggal.html')

    def ubahPasswordBaru(self):
        if request.method == 'POST':
            new_pw = request.form['new_password']
            confirm_pw = request.form['confirm_password']

            if new_pw != confirm_pw:
                flash('Konfirmasi password salah.')
            else:
                username = session.get('reset_user')
                hash_pw = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt())

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE User_Tabel SET password = %s WHERE username = %s", (hash_pw.decode('utf-8'), username))
                conn.commit()
                conn.close()
                flash('Password berhasil diperbarui.')
                return redirect(url_for('login_route'))
        return render_template('auth/reset.html')