<?php
// index.php
session_start();
if (isset($_SESSION['user_id']) && isset($_SESSION['role'])) {
    header('Location: /' . $_SESSION['role'] . '/dashboard.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NusaCarbon - Transparent. Verified. Tokenized Carbon Credits.</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        /* Theme Variables */
        :root {
            --bg-main: #f8fafc;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --card-bg: #ffffff;
            --card-border: rgba(0, 0, 0, 0.08);
            --card-hover-border: rgba(16, 185, 129, 0.3);
            --wave-1: rgba(15, 23, 42, 0.2);
            --wave-2: rgba(16, 185, 129, 0.3);
        }

        [data-theme="dark"] {
            --bg-main: #02120b;
            /* Deep dark teal/forest gradient hint */
            --text-main: #ffffff;
            --text-muted: #94a3b8;
            --card-bg: rgba(255, 255, 255, 0.03);
            --card-border: rgba(255, 255, 255, 0.08);
            --card-hover-border: rgba(16, 185, 129, 0.4);
            --wave-1: rgba(255, 255, 255, 0.15);
            --wave-2: rgba(16, 185, 129, 0.25);
        }

        body,
        html {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            width: 100%;
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
            background: var(--bg-main);
            color: var(--text-main);
            transition: background-color 0.4s ease, color 0.4s ease;
            overflow-x: hidden;
        }

        /* Override main.css strict colors */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--text-main) !important;
            line-height: 1.2;
        }

        p {
            color: inherit;
            line-height: 1.6;
        }

        .text-muted {
            color: var(--text-muted) !important;
        }

        /* Ambient Corporate Video/Canvas Background */
        #waveCanvas {
            position: fixed;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            mix-blend-mode: multiply;
            opacity: 1;
            pointer-events: none;
        }

        [data-theme="dark"] #waveCanvas {
            mix-blend-mode: screen;
        }

        .main-wrapper {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Hero Typography */
        .hero-title {
            font-size: 6rem;
            letter-spacing: -0.05em;
            color: var(--text-main);
            font-weight: 800;
            margin-bottom: 24px;
            margin-top: 60px;
        }

        @media(max-width: 768px) {
            .hero-title {
                font-size: 4rem;
            }
        }

        .hero-desc {
            color: var(--text-muted);
            font-size: 1.25rem;
            line-height: 1.6;
            max-width: 650px;
            margin: 0 auto;
        }

        /* Role Cards */
        .role-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            margin-top: 60px;
            width: 100%;
            max-width: 1000px;
            padding: 0 24px;
        }

        @media (min-width: 768px) {
            .role-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        .role-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 32px;
            border-radius: 20px;
            text-align: left;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-main) !important;
            text-decoration: none;
            display: flex;
            align-items: flex-start;
            gap: 20px;
        }

        .role-card:hover {
            transform: translateY(-4px);
            border-color: var(--card-hover-border);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
        }

        [data-theme="dark"] .role-card:hover {
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .icon-wrapper {
            padding: 16px;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .role-card.buyer .icon-wrapper {
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
        }

        .role-card.owner .icon-wrapper {
            background: rgba(14, 165, 233, 0.1);
            color: #0ea5e9;
        }

        .role-card.verifier .icon-wrapper {
            background: rgba(139, 92, 246, 0.1);
            color: #8b5cf6;
        }

        .role-card.admin .icon-wrapper {
            background: var(--card-border);
            color: var(--text-main);
        }

        /* Blockchain Stats Section */
        .network-stats {
            margin-top: 100px;
            padding: 60px 24px;
            width: 100%;
            max-width: 1100px;
            display: flex;
            flex-direction: column;
            gap: 40px;
        }

        @media (min-width: 900px) {
            .network-stats {
                flex-direction: row;
                justify-content: space-between;
                align-items: stretch;
            }

            .network-stats .col-left {
                flex: 1;
                padding-right: 60px;
                border-right: 1px solid var(--card-border);
            }

            .network-stats .col-right {
                flex: 1.2;
                padding-left: 60px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                gap: 40px;
            }
        }

        .network-stats h2 {
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -1px;
            margin-bottom: 20px;
        }

        .network-stats p {
            font-size: 1.1rem;
            color: var(--text-muted);
            line-height: 1.6;
        }

        .stat-item {
            display: flex;
            align-items: center;
            gap: 24px;
        }

        .stat-icon {
            color: var(--text-muted);
            opacity: 0.5;
        }

        .stat-value {
            font-size: 3.5rem;
            font-family: monospace;
            font-weight: 700;
            letter-spacing: -2px;
            line-height: 1;
            margin-bottom: 8px;
            color: var(--text-main);
        }

        .stat-label {
            color: var(--text-muted);
            font-size: 0.95rem;
            font-weight: 500;
        }

        /* Extended Info Layout */
        .ecosystem-section {
            margin-top: 40px;
            margin-bottom: 80px;
            width: 100%;
            max-width: 1100px;
            padding: 0 24px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 32px;
            margin-top: 40px;
        }

        @media (min-width: 768px) {
            .info-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        .info-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 40px 32px;
            border-radius: 24px;
            text-align: left;
        }

        .info-card h3 {
            font-size: 1.4rem;
            margin-bottom: 16px;
            color: var(--text-main);
            font-weight: 700;
        }

        .info-card p {
            font-size: 0.95rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin: 0;
        }

        .info-card .num {
            font-family: monospace;
            font-size: 1.2rem;
            margin-bottom: 24px;
            color: #10b981;
            font-weight: bold;
        }

        /* Fat Footer */
        .fat-footer {
            width: 100%;
            border-top: 1px solid var(--card-border);
            padding: 80px 24px 40px 24px;
            background: rgba(0, 0, 0, 0.01);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .fat-footer-inner {
            width: 100%;
            max-width: 1100px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 60px;
        }

        @media (min-width: 768px) {
            .fat-footer-inner {
                grid-template-columns: 2fr 1fr 1fr;
            }
        }

        .fat-footer .brand {
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.5rem;
        }

        .fat-footer p {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.6;
            max-width: 300px;
            margin-bottom: 24px;
        }

        .social-icons {
            display: flex;
            gap: 16px;
            color: var(--text-muted);
        }

        .social-icons svg {
            cursor: pointer;
            transition: 0.2s;
        }

        .social-icons svg:hover {
            color: var(--text-main);
        }

        .footer-col h4 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--text-main);
        }

        .footer-col ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .footer-col ul li {
            margin-bottom: 12px;
        }

        .footer-col ul li a {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            transition: 0.2s;
        }

        .footer-col ul li a:hover {
            color: var(--text-main);
        }
    </style>
</head>
<!-- Initial Theme Check -->
<script>
    const savedTheme = localStorage.getItem('nusaTheme') || 'light';
    if (savedTheme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
</script>

<body>

    <!-- Minimalist Corporate Canvas Background -->
    <canvas id="waveCanvas"></canvas>

    <div class="main-wrapper">

        <header
            style="width: 100%; padding: 24px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--card-border);">
            <div
                style="display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 1.4rem; letter-spacing: -0.5px;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#10b981"
                    stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="28" height="28">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
                    <path d="M2 22 12 12" />
                </svg>
                NusaCarbon
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <!-- Theme Toggle Button -->
                <button id="themeToggleBtn"
                    style="background: transparent; border: none; cursor: pointer; color: var(--text-main); display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--card-border);">
                    <i data-lucide="moon" width="18" id="themeIcon"></i>
                </button>
                <a href="/login.php"
                    style="background: var(--text-main) !important; color: var(--bg-main) !important; padding: 10px 24px; border-radius: 50px; text-decoration: none; font-size: 14px; font-weight: 600; display: inline-block;">Log
                    In</a>
            </div>
        </header>

        <main
            style="width: 100%; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 60px 24px 0 24px;">
            <div class="fade-up">
                <span
                    style="background: rgba(16,185,129,0.1); color: #10b981; padding: 6px 16px; border-radius: 50px; font-size: 13px; font-weight: 600; border: 1px solid rgba(16,185,129,0.2); letter-spacing: 0.5px; text-transform: uppercase;">Infrastruktur
                    Berkelanjutan</span>

                <h1 class="hero-title">Pasar emisi<br>untuk bumi kita.</h1>
                <p class="hero-desc">Sistem jaringan mutakhir untuk melacak dan memverifikasi siklus kredit iklim dunia
                    secara mutlak, transparan, dan tidak dapat dimanipulasi.</p>

                <div style="margin-top: 40px; display: flex; gap: 16px; justify-content: center;">
                    <a href="/login.php" class="btn-primary"
                        style="background: var(--text-main) !important; color: var(--bg-main) !important; border: none; padding: 14px 32px; font-weight: bold; font-size: 16px; border-radius: 50px; text-decoration: none; display: flex; align-items: center; gap: 8px;">Masuk
                        <i data-lucide="arrow-right" width="18"></i></a>
                    <a href="/register.php" class="btn-outline"
                        style="background: var(--card-bg); border: 1px solid var(--card-border); color: var(--text-main) !important; padding: 14px 32px; font-weight: 600; font-size: 16px; border-radius: 50px; text-decoration: none; backdrop-filter: blur(10px);">Daftar
                        Sekarang</a>
                </div>
            </div>

            <!-- Role Grid -->
            <div class="role-grid fade-up" style="animation-delay: 100ms;">
                <a href="/login.php?role=buyer" class="role-card buyer">
                    <div class="icon-wrapper"><i data-lucide="wallet" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Blokchain Wallet</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: var(--text-muted);">Beli & ofset emisi (burn)
                            karbon melalui pasar secara langsung.</p>
                    </div>
                </a>
                <a href="/login.php?role=owner" class="role-card owner">
                    <div class="icon-wrapper"><i data-lucide="tree-pine" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Project Owner</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: var(--text-muted);">Mendaftarkan tanah, hutan,
                            dan proyek energi terbarukan.</p>
                    </div>
                </a>
                <a href="/login.php?role=verifier" class="role-card verifier">
                    <div class="icon-wrapper"><i data-lucide="shield-check" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Sistem Verifier</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: var(--text-muted);">Platform dMRV untuk pihak
                            ketiga dan auditor lingkungan.</p>
                    </div>
                </a>
                <a href="/login.php?role=admin" class="role-card admin">
                    <div class="icon-wrapper"><i data-lucide="settings-2" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Pusat Regulasi</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: var(--text-muted);">KYC terpadu guna memastikan
                            keamanan antar entitas lembaga.</p>
                    </div>
                </a>
            </div>

            <!-- Authentic Ecosystem Text -->
            <div class="ecosystem-section fade-up" style="animation-delay: 200ms; text-align: left; margin-top: 100px;">
                <h2 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 12px;">Solusi iklim
                    yang nyata</h2>
                <p style="font-size: 1.1rem; color: var(--text-muted); max-width: 600px;">Setiap metrik lingkungan
                    diaudit dan dibuktikan secara matematis, mencegah terjadinya greenwashing (klaim palsu) pada level
                    korporat.</p>

                <div class="info-grid">
                    <div class="info-card">
                        <div class="num">01</div>
                        <h3>Proses Tokenisasi</h3>
                        <p>Aset fisik seperti kemampuan penyerapan CO₂ lahan gambut divalidasi dan diubah menjadi aset
                            digital di dalam buku besar NusaCarbon agar dapat ditransaksikan tanpa kehilangan jejak
                            audit.</p>
                    </div>
                    <div class="info-card">
                        <div class="num">02</div>
                        <h3>digital MRV</h3>
                        <p>Pemantauan (Monitoring), Pelaporan (Reporting), dan Verifikasi secara digital menggantikan
                            proses manual tradisional yang rawan fraud, memastikan akurasi emisi hingga ke level gram.
                        </p>
                    </div>
                    <div class="info-card">
                        <div class="num">03</div>
                        <h3>Pembakaran Absolut (Burning)</h3>
                        <p>Ketika perusahaan menebus karbon kreditnya, sistem secara permanen akan memusnahkan token
                            tersebut dari sirkulasi pasar (Retire) untuk mencegah penghitungan ganda (Double Counting).
                        </p>
                    </div>
                </div>
            </div>

            <!-- Live Network Stats -->
            <div class="network-stats fade-up" style="animation-delay: 300ms;">
                <div class="col-left" style="text-align: left;">
                    <h2>Kecepatan dan Skalabilitas Mutlak</h2>
                    <p>Fondasi utama dari perdagangan iklim masa depan. NusaCarbon dirancang untuk menangani likuiditas
                        aset lingkungan terbesar di Asia tanpa hambatan throughput.</p>
                </div>
                <div class="col-right" style="text-align: left;">
                    <div class="stat-item">
                        <div class="stat-icon"><i data-lucide="activity" width="32" height="32"></i></div>
                        <div>
                            <div id="liveTotalTx" class="stat-value">503,272,567,466</div>
                            <div class="stat-label">Total instruksi yang telah diproses buku besar</div>
                        </div>
                    </div>
                    <div class="stat-item" style="border-top: 1px solid var(--card-border); padding-top: 40px;">
                        <div class="stat-icon"><i data-lucide="zap" width="32" height="32"></i></div>
                        <div>
                            <div id="liveTps" class="stat-value text-green-400" style="color: #10b981;">3.245</div>
                            <div class="stat-label">Transaksi jaringan per detik (TPS)</div>
                        </div>
                    </div>
                </div>
            </div>

        </main>

        <!-- Fat Footer -->
        <footer class="fat-footer">
            <div class="fat-footer-inner">
                <div>
                    <div class="brand">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#10b981"
                            stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="28" height="28">
                            <path
                                d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
                            <path d="M2 22 12 12" />
                        </svg>
                        NusaCarbon
                    </div>
                    <p>Dikelola dan diawasi oleh NusaCarbon Foundation. Semua infrastruktur kode bersifat tertutup
                        digunakan untuk keperluan tugas kuliah Pemograman Web (Simulasi Akademik).</p>
                    <p style="font-size: 0.85rem; margin-top: 40px;">&copy; 2026 NusaCarbon Foundation. <br>Hak Cipta
                        Dilindungi Undang-Undang.</p>
                </div>

                <div class="footer-col">
                    <h4>Platform</h4>
                    <ul>
                        <li><a href="#">Arsitektur Sistem</a></li>
                        <li><a href="#">Whitepaper dMRV</a></li>
                        <li><a href="#">Standar Karbon Terbuka</a></li>
                        <li><a href="#">Audit Independen</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h4>Terhubung</h4>
                    <ul>
                        <li><a href="#">Dukungan Teknis</a></li>
                        <li><a href="#">Media Kit & Brand</a></li>
                        <li><a href="#">Github</a></li>
                        <li><a href="#">Kebijakan Privasi</a></li>
                    </ul>
                </div>
            </div>

            <div style="width: 100%; max-width: 1100px; display: flex; justify-content: flex-end; margin-top: 40px;">
                <div class="social-icons">
                    <i data-lucide="youtube" width="20"></i>
                    <i data-lucide="twitter" width="20"></i>
                    <i data-lucide="github" width="20"></i>
                    <i data-lucide="mail" width="20"></i>
                </div>
            </div>
        </footer>
    </div>

    <!-- Scripts -->
    <script>
        lucide.createIcons();

        // Theme Toggle Logic
        const toggleBtn = document.getElementById('themeToggleBtn');
        const themeIcon = document.getElementById('themeIcon');
        const root = document.documentElement;

        function updateIcon() {
            if (root.getAttribute('data-theme') === 'dark') {
                themeIcon.setAttribute('data-lucide', 'sun');
            } else {
                themeIcon.setAttribute('data-lucide', 'moon');
            }
            lucide.createIcons();
        }
        updateIcon();

        toggleBtn.addEventListener('click', () => {
            const current = root.getAttribute('data-theme');
            if (current === 'dark') {
                root.removeAttribute('data-theme');
                localStorage.setItem('nusaTheme', 'light');
            } else {
                root.setAttribute('data-theme', 'dark');
                localStorage.setItem('nusaTheme', 'dark');
            }
            updateIcon();
        });

        // Live Counters Logic
        let totalTx = 503272567466;
        const liveTotalTxEl = document.getElementById('liveTotalTx');
        const liveTpsEl = document.getElementById('liveTps');

        setInterval(() => {
            totalTx += Math.floor(Math.random() * 50) + 10;
            liveTotalTxEl.innerText = totalTx.toLocaleString('en-US'); // Will show commas
        }, 80);

        setInterval(() => {
            const tps = 3000 + Math.floor(Math.random() * 999);
            liveTpsEl.innerText = (tps / 1000).toFixed(3);
        }, 1000);


        // Corporate Minimalist Wave Canvas
        const canvas = document.getElementById('waveCanvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            let width, height;
            let time = 0;

            function resize() {
                width = window.innerWidth;
                height = window.innerHeight;
                canvas.width = width * 2;
                canvas.height = height * 2;
                ctx.scale(2, 2);
            }
            window.addEventListener('resize', resize);
            resize();

            function animate() {
                ctx.clearRect(0, 0, width, height);
                time += 0.003;

                // Fetch colors from CSS variable for dynamic theme switching
                const waveStyle = getComputedStyle(document.documentElement);
                const color1 = waveStyle.getPropertyValue('--wave-1').trim() || 'rgba(15, 23, 42, 0.04)';
                const color2 = waveStyle.getPropertyValue('--wave-2').trim() || 'rgba(16, 185, 129, 0.05)';

                const waves = [
                    { color: color1, speed: 0.5, freq: 0.001, amp: 200 },
                    { color: color2, speed: 0.8, freq: 0.002, amp: 180 }
                ];

                waves.forEach((wave, i) => {
                    ctx.beginPath();
                    ctx.moveTo(0, height / 2);
                    for (let x = 0; x <= width; x += 10) {
                        let y = Math.sin((x * wave.freq) + (time * wave.speed) + i) * wave.amp * Math.sin(time + i);
                        y += Math.sin(x * 0.001 - time) * 80;
                        ctx.lineTo(x, height / 2 + y);
                    }
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = wave.color;
                    ctx.stroke();
                });

                requestAnimationFrame(animate);
            }
            animate();
        }
    </script>
</body>

</html>