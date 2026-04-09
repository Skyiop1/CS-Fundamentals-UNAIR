# NusaCarbon - HTML & CSS Starter Project

Implementasi awal website **NusaCarbon (Nusantara Carbon Token Exchange Platform)** menggunakan **HTML5 + CSS3**.

## Struktur Folder

```text
NusaCarbon-HTML-CSS/
├── index.html
├── login.html
├── register.html
├── marketplace.html
├── project-detail.html
├── buyer-dashboard.html
├── owner-dashboard.html
├── form-project.html
├── form-upload.html
├── data-tables.html
├── README.md
└── assets/
    ├── css/
    │   └── style.css
    └── img/
        ├── logo.svg
        ├── hero-visual.svg
        ├── map-project.svg
        ├── chart-mrv.svg
        ├── certificate.svg
        ├── avatar-company.svg
        ├── project-forest.svg
        ├── project-mangrove.svg
        ├── project-solar.svg
        ├── project-wind.svg
        └── project-seedling.svg
```

## Site Map

1. Landing Page / Main Site → `index.html`
2. Login Page → `login.html`
3. Register Page → `register.html`
4. Marketplace Projects → `marketplace.html`
5. Detail Project & MRV Data → `project-detail.html`
6. Dashboard Buyer → `buyer-dashboard.html`
7. Dashboard Project Owner → `owner-dashboard.html`
8. Form Input Project → `form-project.html`
9. Form Upload Dokumen Verifikasi → `form-upload.html`
10. Tabel Data Token / Transaksi / Retirement / Sertifikat → `data-tables.html`

## Catatan Implementasi

- Menggunakan **semantic HTML5**: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`
- Menggunakan **meta tag dasar**: charset, viewport, description, title
- Menggunakan **form validation** dasar: `required`, `type="email"`, `minlength`, `accept`
- Menggunakan **tabel semantik**: `thead`, `tbody`, `th`, `td`
- Menggunakan **CSS eksternal** di `assets/css/style.css`
- Layout dibuat dengan **Flexbox**, **CSS Grid**, dan **media query**
- Konten masih berupa **dummy data** agar mudah dikembangkan ke tahap JavaScript/backend

## Cara Menjalankan

1. Extract file ZIP.
2. Buka folder project.
3. Jalankan `index.html` langsung di browser.
4. Navigasi antar halaman menggunakan menu yang tersedia.

## Saran Tahap Selanjutnya

- Tambahkan JavaScript untuk interaksi filter marketplace
- Tambahkan backend login/register
- Hubungkan form project ke database MySQL
- Integrasikan smart contract / API blockchain secara bertahap
