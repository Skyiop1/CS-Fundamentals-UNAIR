# 🌿 NusaCarbon Web Platform

NusaCarbon adalah prototipe aplikasi web *marketplace* kredit karbon yang memanfaatkan simulasi teknologi Blockchain (append-only ledger). Platform ini diciptakan untuk memfasilitasi transaksi sertifikat penurunan emisi antara pemilik proyek lingkungan (Project Owner), lembaga verifikator, dan pembeli (Buyer/Perusahaan) dengan transparan dan terdesentralisasi.

## 🚀 Fitur Utama
Sistem ini menggunakan arsitektur **Role-Based Access Control (RBAC)** untuk 4 aktor utama:
1. **Buyer (Pembeli)**: Memiliki dompet digital (Web3 Wallet mock), melihat katalog marketplace, membeli token karbon, dan membakar (*retire*) token untuk mendapatkan Sertifikat Karbon Offset.
2. **Project Owner**: Mengajukan proyek hijau (misal: Hutan kemasyarakatan, Mangrove) ke dalam platform.
3. **Verifier**: Memvalidasi kualitas proyek secara independen dan mencetak (*minting*) Token Karbon (tCO₂e) baru.
4. **Admin**: Mengelola ekosistem secara keseluruhan.

> **Transparansi Blockchain:** Setiap transaksi *transfer*, *mint*, dan *retire* dicatat ke dalam tabel `blockchain_ledger` murni (tanpa fungsi `UPDATE` atau `DELETE`) yang dikunci dengan algoritma *cryptographic hash* `SHA-256`.

---

## 🛠️ Tech Stack
Platform ini dibangun dengan pendekatan *Native* untuk memastikan pemahaman pondasi yang kuat terhadap ekosistem web:
- **Backend:** PHP 8.2 (Native / No Framework) + PDO (Data Objects)
- **Database:** MySQL 8.0 murni (Full PDM Architecture)
- **Frontend:** HTML5, CSS3 Variables (Brand: Emerald & Teal), Vanilla Javascript, Chart.js, Lucide Icons.
- **Infrastruktur:** Docker & Docker Compose (Containerized).

---

## 💻 Panduan Instalasi (Development)

Sistem ini didesain agar sangat mudah dijalankan menggunakan **Docker**. Anda tidak perlu mengunduh dan mengatur PHP/XAMPP/MySQL di laptop secara manual.

### Prasyarat:
- Pastikan **Docker Desktop** atau Docker Engine sudah terinstal di komputer/laptop Anda.

### Langkah-langkah:
1. Buka Terminal atau Command Prompt, lalu arahkan ke folder utama proyek ini:
   ```bash
   cd nusacarbon-web
   ```
2. Jalankan perintah Docker Compose untuk membangun dan menjalankan *container* di *background*:
   ```bash
   docker compose up -d
   ```
   *(Catatan: Proses ini akan otomatis mengunduh image PHP dan MySQL, serta otomatis menjalankan skrip impor tabel dan dataseed ke dalam database).*
3. Tunggu sekitar 15-30 detik hingga server database stabil.
4. Buka browser dan akses aplikasi melalui tautan berikut:
   **[http://localhost:8000](http://localhost:8000)**
5. Jika ingin mematikan server:
   ```bash
   docker compose down
   ```

---

## 🔑 Akun Uji Coba (Mock Data)

Saat pertama kali Docker dijalankan, database akan otomatis berisi akun-akun berikut untuk mempermudah masa *testing*:

| Role | Username / Entitas | Email (Untuk Login) | Password |
|---|---|---|---|
| **Buyer** | Perusahaan Hijau Test | `buyer@nusacarbon.id` | `password123` |
| **Project Owner** | Koperasi Tani Hutan | `owner@nusacarbon.id` | `password123` |
| **Verifier** | Verra Auditor | `verifier@nusacarbon.id` | `password123` |
| **Admin** | Administrator Utama | `admin@nusacarbon.id` | `password123` |

*(Anda bebas membuat akun Buyer baru melalui fitur "Daftar Akun", sistem akan otomatis menghasilkan Alamat Dompet Crypto Mock untuk Anda).*

---

## 🗄️ Akses Database (Opsional)
Jika Anda perlu melihat isi database (misalnya audit ledger atau data token) menggunakan aplikasi seperti **DBeaver** atau **TablePlus**:
- **Host**: `127.0.0.1` / `localhost`
- **Port**: `3306`
- **Database**: `nusacarbon`
- **User**: `nusa_user` (atau `root`)
- **Password**: `nusa_password` (atau `root`)

---

## 🎨 Design System
Platform menggunakan palet yang terinspirasi dari alam, menanamkan rasa kepercayaan dan modernitas Web3. 
- *Primary Color*: `#059669` (Emerald Green)
- *Typography*: Inter (Modern Sans-serif)
- *UI Style* : Flat Modern, Clean Glassmorphism pada Dashboard Cards, Micro-interactions.

---
**© 2026 NusaCarbon** - *Building a Greener Indonesia via Blockchain.*
