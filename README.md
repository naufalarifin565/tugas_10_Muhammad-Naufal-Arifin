# Aplikasi Pendaftaran Siswa

Ini adalah aplikasi web sederhana yang dibangun dengan Flask untuk mengelola data pendaftaran siswa. Aplikasi ini memungkinkan pengguna untuk mendaftar, melihat daftar siswa yang sudah terdaftar, mengedit informasi, dan menghapus data siswa.

## Fitur

  * **Formulir Pendaftaran**: Pengguna dapat memasukkan data diri seperti nama, email, alamat, dan mengunggah foto profil.
  * **Lihat Daftar Siswa**: Menampilkan semua siswa yang telah terdaftar dalam format tabel yang rapi.
  * **CRUD (Create, Read, Update, Delete)**:
      * **Create**: Menambahkan siswa baru ke dalam database.
      * **Read**: Membaca dan menampilkan data siswa dari database.
      * **Update**: Mengedit informasi siswa yang sudah ada, termasuk kemampuan untuk mengubah foto profil.
      * **Delete**: Menghapus data siswa dari database beserta file foto yang terkait.
  * **Upload Foto**: Mengizinkan unggahan foto profil dengan nama file yang unik untuk menghindari konflik.
  * **Notifikasi Flash**: Memberikan umpan balik kepada pengguna untuk setiap aksi yang berhasil atau gagal (contoh: 'Data siswa berhasil ditambahkan\!').

## Teknologi yang Digunakan

  * **Backend**: Flask (Python)
  * **Frontend**: HTML, CSS
  * **Database**: MySQL
  * **Library Python**:
      * `Flask`: Kerangka kerja web.
      * `mysql-connector-python`: Untuk menghubungkan aplikasi dengan database MySQL.
      * `Werkzeug`: Untuk menangani unggahan file yang aman.

## Instalasi dan Setup

Berikut adalah langkah-langkah untuk menjalankan proyek ini secara lokal.

### 1\. Prasyarat

  * Python 3.x
  * PIP (Package Installer for Python)
  * Server Database MySQL

### 2\. Kloning Repositori

```bash
git clone https://github.com/naufalarifin565/tugas_10_muhammad-naufal-arifin.git
cd tugas_10_muhammad-naufal-arifin
```

### 3\. Buat dan Aktifkan Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4\. Instal Dependensi

Buat file `requirements.txt` dan isi dengan:

```
Flask
mysql-connector-python
Werkzeug
```

Kemudian, jalankan perintah berikut:

```bash
pip install -r requirements.txt
```

### 5\. Konfigurasi Database

1.  Pastikan server MySQL Anda berjalan.
2.  Buat database baru dengan nama `db_pendaftaran_siswa`.
    ```sql
    CREATE DATABASE db_pendaftaran_siswa;
    ```
3.  Gunakan database tersebut dan buat tabel `siswa`.
    ```sql
    USE db_pendaftaran_siswa;

    CREATE TABLE siswa (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama_lengkap VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        alamat TEXT NOT NULL,
        foto VARCHAR(255)
    );
    ```
4.  Sesuaikan detail koneksi database di dalam file `app.py` jika diperlukan:
    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'db_pendaftaran_siswa',
        'user': 'root',
        'password': ''  # Sesuaikan dengan password Anda
    }
    ```

### 6\. Jalankan Aplikasi

Setelah semua konfigurasi selesai, jalankan aplikasi dengan perintah:

```bash
python app.py
```

Aplikasi akan berjalan di `http://127.0.0.1:5000`.

## Struktur File

```
.
├── static
│   ├── css
│   │   └── style.css      # File styling utama
│   └── uploads/           # Direktori untuk menyimpan foto yang diunggah
├── templates
│   ├── base.html          # Template dasar dengan navigasi dan footer
│   ├── daftar_siswa.html  # Halaman untuk menampilkan daftar siswa
│   ├── edit_siswa.html    # Halaman untuk mengedit data siswa
│   └── index.html         # Halaman utama dengan form pendaftaran
├── app.py                 # Logika utama aplikasi Flask dan routing
└── README.md

## Tampilan formulir pendaftaran
![image](https://github.com/user-attachments/assets/c2432fa6-e30d-45ac-bf6b-51d250a42409

## Tampilan jika sudah mendaftar/riwayat
![image](https://github.com/user-attachments/assets/9628eafa-64a0-4d5b-970b-3990bbc8a897)

## Pengguna dapat mengedit data diri mereka
![image](https://github.com/user-attachments/assets/345654b7-712a-4f5b-b81e-2f8d3100c890)





```


