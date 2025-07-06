from flask import Flask, render_template, request, redirect, url_for, flash
import os
import uuid
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error

# --- Konfigurasi Aplikasi dan Database ---
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_super_aman'

# Ganti dengan detail koneksi database Anda
DB_CONFIG = {
    'host': 'localhost',
    'database': 'db_pendaftaran_siswa',
    'user': 'root',
    'password': ''
}

# Konfigurasi folder untuk menyimpan file upload
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Membuat folder 'uploads' jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Fungsi Bantuan ---

def get_db_connection():
    """Membuat koneksi ke database MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error saat koneksi ke MySQL: {e}")
        return None

def allowed_file(filename):
    """Mengecek apakah ekstensi file diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rute Aplikasi (Routes) ---

@app.route('/')
def index():
    """Halaman utama yang menampilkan form pendaftaran."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    """Memproses data dari form pendaftaran."""
    nama = request.form['nama']
    email = request.form['email']
    alamat = request.form['alamat']
    foto_filename = 'default.jpg' # Foto default jika tidak ada upload

    if 'foto' in request.files:
        file = request.files['foto']
        if file and file.filename and allowed_file(file.filename):
            # Membuat nama file unik untuk menghindari duplikat
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            foto_filename = unique_filename

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO siswa (nama_lengkap, email, alamat, foto) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nama, email, alamat, foto_filename))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Data siswa berhasil ditambahkan!', 'success')
        return redirect(url_for('daftar_siswa'))
    else:
        flash('Gagal terhubung ke database.', 'danger')
        return redirect(url_for('index'))

@app.route('/daftar-siswa')
def daftar_siswa():
    """Menampilkan daftar semua siswa yang terdaftar."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM siswa ORDER BY id DESC")
        siswa_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('daftar_siswa.html', siswa_list=siswa_list)
    flash('Gagal mengambil data dari database.', 'danger')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_siswa(id):
    """Menampilkan form untuk mengedit data siswa dan memprosesnya."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Proses update data
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']

        # Ambil nama foto lama
        cursor.execute("SELECT foto FROM siswa WHERE id = %s", (id,))
        foto_lama = cursor.fetchone()['foto']
        foto_filename = foto_lama

        # Cek apakah ada file foto baru yang di-upload
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                foto_filename = unique_filename
                # Hapus foto lama jika bukan default
                if foto_lama and foto_lama != 'default.jpg':
                    foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_lama)
                    if os.path.exists(foto_path):
                        os.remove(foto_path)

        query = "UPDATE siswa SET nama_lengkap = %s, email = %s, alamat = %s, foto = %s WHERE id = %s"
        cursor.execute(query, (nama, email, alamat, foto_filename, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Data siswa berhasil diperbarui!', 'success')
        return redirect(url_for('daftar_siswa'))
    else:
        # Tampilkan form edit dengan data yang ada
        cursor.execute("SELECT * FROM siswa WHERE id = %s", (id,))
        siswa = cursor.fetchone()
        cursor.close()
        conn.close()
        if siswa:
            return render_template('edit_siswa.html', siswa=siswa)
        else:
            flash('Data siswa tidak ditemukan.', 'danger')
            return redirect(url_for('daftar_siswa'))


@app.route('/hapus/<int:id>', methods=['POST'])
def hapus_siswa(id):
    """Menghapus data siswa dari database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil nama file foto untuk dihapus dari server
    cursor.execute("SELECT foto FROM siswa WHERE id = %s", (id,))
    hasil = cursor.fetchone()
    if hasil:
        foto_untuk_dihapus = hasil['foto']
        # Hapus file foto jika bukan default
        if foto_untuk_dihapus and foto_untuk_dihapus != 'default.jpg':
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_untuk_dihapus)
            if os.path.exists(foto_path):
                try:
                    os.remove(foto_path)
                except OSError as e:
                    print(f"Error saat menghapus file: {e}")

    # Hapus data dari database
    cursor.execute("DELETE FROM siswa WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Data siswa berhasil dihapus.', 'success')
    return redirect(url_for('daftar_siswa'))


if __name__ == '__main__':
    app.run(debug=True)