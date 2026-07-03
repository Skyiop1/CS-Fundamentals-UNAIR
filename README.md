# Sistem Informasi Peminjaman Buku Perpustakaan Berbasis Web

Aplikasi web perpustakaan berbasis Laravel untuk mendigitalisasi proses pengelolaan data buku, kategori, anggota, serta memproses transaksi peminjaman, pengembalian, dan penghitungan denda keterlambatan secara otomatis. 

Project ini dirancang untuk berjalan menggunakan MySQL baik di lingkungan lokal maupun siap dideploy langsung ke Railway dengan konfigurasi variabel lingkungan (*environment variables*).

---

## Tech Stack

- **Backend**: Laravel 11 (PHP 8.2+)
- **Frontend**: Blade Templates
- **Styling**: Bootstrap 5 & CSS custom
- **Database**: MySQL (mendukung InnoDB dengan foreign key constraints)
- **Deployment**: Railway (menggunakan Nixpacks & MySQL service)

---

## Fitur Utama Sistem

### 1. Panel Admin & Dashboard
- **Admin Dashboard**: Kartu ringkasan statistik (Total Buku, Anggota Aktif, Peminjaman Aktif, Request Menunggu, Buku Terlambat, Akumulasi Denda) beserta daftar transaksi terbaru.
- **CRUD Kategori Buku**: Pengelolaan nama kategori dan deskripsi lengkap dengan deteksi dependensi buku sebelum dihapus.
- **CRUD Data Buku**: Pengelolaan kode buku unik, judul, pengarang, penerbit, tahun terbit, stok buku, sinopsis, dan unggah berkas cover gambar.
- **CRUD Data Anggota**: Pembuatan anggota manual yang menyinkronkan tabel `users` dan `members` dalam DB Transaction, penomoran otomatis `AGT-YYYY-XXXX`, pengaturan status (aktif/inaktif), dan opsi edit password.

### 2. Panel Anggota & Dashboard
- **Member Dashboard**: Ringkasan data personal peminjaman aktif, pengajuan pending, riwayat buku kembali, dan jumlah denda belum dibayar.
- **Katalog & Pencarian Buku**: Galeri card-grid buku dengan pencarian teks (judul/pengarang/kode) dan filter dinamis berbasis kategori.
- **Detail Buku & Pengajuan**: Informasi buku dan cover secara detail. Anggota dapat mengajukan peminjaman buku jika stok masih tersedia dan tidak memiliki riwayat peminjaman aktif untuk buku tersebut.
- **Peminjaman Saya**: Menu riwayat peminjaman personal dengan penyaringan status dan info nominal denda keterlambatan.

### 3. Workflow Peminjaman & Pengembalian
- **Persetujuan Admin**: Admin memproses pengajuan peminjaman (Approve/Reject dengan alasan penolakan).
- **Pengamanan Stok (Race Condition)**: Transaksi disetujui dalam database transaction dengan `lockForUpdate` untuk memastikan stok tidak bernilai negatif saat disetujui bersamaan. Tanggal jatuh tempo diset otomatis 7 hari setelah disetujui.
- **Pengembalian Buku**: Petugas memproses pengembalian buku dengan mencatat tanggal kembali dan catatan kondisi buku. Stok buku akan otomatis bertambah kembali 1.
- **Perhitungan Denda Otomatis**: Jika pengembalian melebihi jatuh tempo, denda akan dihitung otomatis dengan rumus:
  `late_days = max(0, return_date - due_date)`
  `fine_amount = late_days × 1000`
- **Pelunasan Denda**: Admin dapat mencatat status denda menjadi lunas (`paid`) saat anggota melakukan pembayaran denda di kasir.

---

## Role & Hak Akses

- **Admin**: Petugas perpustakaan yang memiliki kendali penuh atas manajemen data buku, kategori, anggota, persetujuan peminjaman, pemrosesan pengembalian, dan verifikasi pelunasan denda.
- **Anggota**: Pengguna perpustakaan yang dapat mencari/melihat katalog buku, melakukan pengajuan peminjaman, serta melacak status dan denda peminjaman miliknya sendiri.

*Sistem dilengkapi keamanan tingkat tinggi (Admin Middleware & Owner-based check) untuk mencegah manipulasi parameter ID URL oleh anggota.*

---

## Akun Demo Default

Sistem menyediakan akun siap pakai melalui seeder database:

### Akun Admin
- **Email**: `admin@perpus.test`
- **Password**: `password`

### Akun Anggota
- **Email**: `anggota@perpus.test`
- **Password**: `password`

---

## Instalasi Lokal

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal:

### 1. Prasyarat
- PHP 8.2 atau lebih baru
- Composer
- MySQL Database Server (XAMPP / Laragon / Docker)

### 2. Kloning & Install Dependency
Masuk ke direktori project Anda, lalu jalankan:
```bash
composer install
```

### 3. Salin Konfigurasi Environment
```bash
cp .env.example .env
```

### 4. Generate Application Key
```bash
php artisan key:generate
```

### 5. Atur Database di `.env`
Buka file `.env` yang baru dibuat dan sesuaikan kredensial MySQL lokal Anda:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=perpustakaan
DB_USERNAME=root
DB_PASSWORD=
```
*Catatan: Pastikan Anda sudah membuat database kosong bernama `perpustakaan` di phpMyAdmin atau DBMS Anda.*

### 6. Jalankan Migrasi & Seeding Data
Jalankan perintah berikut untuk membuat tabel dan mengisi data demo (admin, anggota, kategori, dan buku contoh):
```bash
php artisan migrate --seed
```

### 7. Buat Symbolic Link Storage
Guna menampilkan gambar cover buku yang diunggah secara lokal, hubungkan direktori storage:
```bash
php artisan storage:link
```

### 8. Jalankan Local Server
Jalankan server bawaan Laravel:
```bash
php artisan serve
```
Aplikasi dapat diakses melalui browser di: [http://localhost:8000](http://localhost:8000)

---

## Deployment ke Railway

Aplikasi ini sudah dikonfigurasi menggunakan Nixpacks (`nixpacks.toml`) dan siap untuk dipublikasikan langsung ke Railway.

### 1. Langkah Persiapan
1. Pastikan project Anda sudah di-commit ke Git dan di-push ke repository GitHub.
2. Buat akun di [Railway.app](https://railway.app).

### 2. Setup Project di Railway
1. Di dashboard Railway, klik **New Project** dan hubungkan dengan repository GitHub project Anda.
2. Tambahkan layanan database bawaan Railway dengan mengklik **+ New** -> **Database** -> **Add MySQL**.
3. Railway secara otomatis akan melakukan build menggunakan setelan yang tertera di `nixpacks.toml`.

### 3. Setelan Environment Variables (Variables)
Di layanan aplikasi web Anda di Railway, tambahkan konfigurasi variabel lingkungan berikut di tab **Variables**:

```env
APP_NAME="Sistem Informasi Perpustakaan"
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:hasil-dari-php-artisan-key-generate
APP_URL=https://nama-project-anda.up.railway.app
APP_TIMEZONE=Asia/Jakarta

DB_CONNECTION=mysql
DB_HOST=${{MySQL.MYSQLHOST}}
DB_PORT=${{MySQL.MYSQLPORT}}
DB_DATABASE=${{MySQL.MYSQLDATABASE}}
DB_USERNAME=${{MySQL.MYSQLUSER}}
DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}
```
*Railway akan otomatis menyuntikkan kredensial MySQL secara dinamis menggunakan sintaks referensi variabel di atas.*

### 4. Eksekusi Migrasi di Server Railway
Setelah proses deploy web service dan database MySQL selesai di Railway, jalankan migrasi database di server produksi menggunakan terminal Railway (*Railway Shell* atau tab *Deployments* -> *Reference*):
```bash
php artisan migrate --seed --force
```

---

## Link Project & Demo

- **GitHub Repository**: [https://github.com/Skyiop1/CS-Fundamentals-UNAIR/tree/main/Sistem%20Informasi%20Perpustakaan](https://github.com/Skyiop1/CS-Fundamentals-UNAIR/tree/main/Sistem%20Informasi%20Perpustakaan)
- **Demo Website**: [https://your-project.up.railway.app](https://your-project.up.railway.app)
- **Custom Domain**: [https://yourdomain.com](https://yourdomain.com)
