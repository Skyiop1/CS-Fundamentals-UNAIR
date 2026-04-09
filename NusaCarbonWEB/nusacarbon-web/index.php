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
    <link rel="stylesheet" href="/assets/css/dashboard.css">
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        body, html {
            margin: 0; padding: 0; 
            width: 100%; min-height: 100vh;
            font-family: 'Inter', sans-serif;
            background: #000;
            color: #fff;
            overflow-x: hidden;
        }

        /* Ambient Video/Canvas Background */
        #waveCanvas {
            position: fixed; inset: 0; width: 100%; height: 100%; 
            z-index: 0; mix-blend-mode: screen; opacity: 0.8;
            pointer-events: none;
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
            font-size: 5rem;
            letter-spacing: -0.04em;
            color: #ffffff;
            font-weight: 800;
            margin-bottom: 24px;
            margin-top: 60px;
            background: linear-gradient(to right, #ffffff, #a1a1aa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        @media(max-width: 768px) { .hero-title { font-size: 3.5rem; } }

        .hero-desc {
            color: #a1a1aa;
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
        @media (min-width: 768px) { .role-grid { grid-template-columns: 1fr 1fr; } }
        
        .role-card {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            backdrop-filter: blur(20px);
            padding: 32px;
            border-radius: 24px;
            text-align: left;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: white !important;
            text-decoration: none;
            display: flex;
            align-items: flex-start;
            gap: 20px;
        }
        .role-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.06) !important;
            border-color: rgba(16,185,129,0.3) !important;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
        }
        .icon-wrapper {
            padding: 16px; border-radius: 16px;
            display: inline-flex; align-items: center; justify-content: center;
        }
        .role-card.buyer .icon-wrapper { background: rgba(16,185,129,0.1); color: #34d399; }
        .role-card.owner .icon-wrapper { background: rgba(56,189,248,0.1); color: #7dd3fc; }
        .role-card.verifier .icon-wrapper { background: rgba(139,92,246,0.1); color: #c4b5fd; }
        .role-card.admin .icon-wrapper { background: rgba(226,232,240,0.1); color: #f1f5f9; }

        /* Blockchain Stats Section (Solana Style) */
        .network-stats {
            margin-top: 100px;
            margin-bottom: 60px;
            width: 100%;
            max-width: 1100px;
            padding: 0 24px;
            display: flex;
            flex-direction: column;
            gap: 40px;
        }
        @media (min-width: 900px) {
            .network-stats { flex-direction: row; justify-content: space-between; align-items: stretch; }
            .network-stats .col-left { flex: 1; padding-right: 60px; border-right: 1px solid rgba(255,255,255,0.1); }
            .network-stats .col-right { flex: 1.2; padding-left: 60px; display: flex; flex-direction: column; justify-content: center; gap: 40px; }
        }
        
        .network-stats h2 { font-size: 2.8rem; font-weight: 800; line-height: 1.2; letter-spacing: -1px; margin-bottom: 20px;}
        .network-stats p { font-size: 1.1rem; color: #a1a1aa; line-height: 1.6; }
        
        .stat-item { display: flex; align-items: center; gap: 24px; }
        .stat-icon { color: #a1a1aa; opacity: 0.5; }
        .stat-value { 
            font-size: 3rem; font-family: monospace; font-weight: 700; 
            letter-spacing: -2px; line-height: 1; margin-bottom: 8px;
            color: #fff;
        }
        .stat-label { color: #a1a1aa; font-size: 0.95rem; font-weight: 500;}

    </style>
</head>
<body>
    
    <!-- Animated Video Background -->
    <canvas id="waveCanvas"></canvas>

    <div class="main-wrapper">
        
        <!-- Navbar Mock -->
        <header style="width: 100%; padding: 24px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <div style="display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.2rem; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="24" height="24">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 22 12 12"/>
                </svg>
                NusaCarbon
            </div>
            <div>
                <a href="/login.php" class="btn-outline" style="border: 1px solid rgba(255,255,255,0.2); color: white; padding: 8px 20px; border-radius: 50px; text-decoration: none; font-size: 14px;">Log In</a>
            </div>
        </header>

        <!-- Main Hero -->
        <main style="width: 100%; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 40px 24px;">
            <div class="fade-up">
                <span style="background: rgba(16,185,129,0.1); color: #34d399; padding: 6px 16px; border-radius: 50px; font-size: 13px; font-weight: 600; border: 1px solid rgba(16,185,129,0.2); letter-spacing: 0.5px; text-transform: uppercase;">Awan Hijau Indonesia</span>
                
                <h1 class="hero-title">Pasar masa depan<br>untuk setiap aset bumi.</h1>
                <p class="hero-desc">NusaCarbon adalah ekosistem desentralisasi berkinerja tinggi yang memverifikasi, melacak, dan memperdagangkan kredit iklim secara mutlak tanpa pihak ketiga.</p>
                
                <div style="margin-top: 40px; display: flex; gap: 16px; justify-content: center;">
                    <a href="/login.php" class="btn-primary" style="background: white !important; color: #000 !important; border: none; padding: 14px 32px; font-weight: bold; font-size: 16px; border-radius: 50px; text-decoration: none;">Explore &rarr;</a>
                    <a href="/buyer/marketplace.php" class="btn-outline" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 14px 32px; font-weight: 600; font-size: 16px; border-radius: 50px; text-decoration: none; backdrop-filter: blur(10px);">Guest View</a>
                </div>
            </div>

            <!-- Role Grid -->
            <div class="role-grid fade-up" style="animation-delay: 100ms;">
                <a href="/login.php?role=buyer" class="role-card buyer">
                    <div class="icon-wrapper"><i data-lucide="wallet" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Buyer Wallet</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: rgba(255,255,255,0.6);">Beli & hapus token kredit karbon transparan.</p>
                    </div>
                </a>
                <a href="/login.php?role=owner" class="role-card owner">
                    <div class="icon-wrapper"><i data-lucide="tree-pine" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Project Owner</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: rgba(255,255,255,0.6);">Daftarkan proyek & tokenisasi sertifikat iklim.</p>
                    </div>
                </a>
                <a href="/login.php?role=verifier" class="role-card verifier">
                    <div class="icon-wrapper"><i data-lucide="shield-check" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Global Verifiers</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: rgba(255,255,255,0.6);">Sistem dMRV untuk auditor lingkungan independen.</p>
                    </div>
                </a>
                <a href="/login.php?role=admin" class="role-card admin">
                    <div class="icon-wrapper"><i data-lucide="settings-2" width="28"></i></div>
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">Platform Node Admin</h3>
                        <p style="margin: 0; font-size: 0.95rem; color: rgba(255,255,255,0.6);">Pengelolaan ekosistem & validasi peserta KYC.</p>
                    </div>
                </a>
            </div>

            <!-- NEW: Live Network Stats Section -->
            <div class="network-stats fade-up" style="animation-delay: 200ms;">
                <div class="col-left" style="text-align: left;">
                    <h2>Ekosistem keuangan terdesentralisasi<br>dengan kecepatan maksimum</h2>
                    <p>Platform nomor satu untuk startup, negara, dan korporasi ESG. Mengamankan rantai pasok kredit iklim dengan TPS nyata tertinggi di Asia.</p>
                </div>
                <div class="col-right" style="text-align: left;">
                    <div class="stat-item">
                        <div class="stat-icon"><i data-lucide="activity" width="32" height="32"></i></div>
                        <div>
                            <div id="liveTotalTx" class="stat-value">503,272,567,466</div>
                            <div class="stat-label">Total transaksi hingga saat ini</div>
                        </div>
                    </div>
                    <div class="stat-item" style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 40px;">
                        <div class="stat-icon"><i data-lucide="zap" width="32" height="32"></i></div>
                        <div>
                            <div id="liveTps" class="stat-value text-green-400" style="color: #34d399;">3.245</div>
                            <div class="stat-label">Transaksi per detik</div>
                        </div>
                    </div>
                </div>
            </div>

        </main>

        <footer style="width: 100%; border-top: 1px solid rgba(255,255,255,0.1); text-align: center; padding: 40px; color: rgba(255,255,255,0.5); font-size: 0.9rem;">
            <p>&copy; 2026 NusaCarbon Mainnet. Secure.</p>
        </footer>
    </div>

    <!-- Scripts -->
    <script>
        lucide.createIcons();

        // 1. Live Counters Logic
        let totalTx = 503272567466; // Initial huge number
        const liveTotalTxEl = document.getElementById('liveTotalTx');
        const liveTpsEl = document.getElementById('liveTps');

        // Update Total TX extremely fast
        setInterval(() => {
            // Add a random amount of transactions (e.g. 10 to 60 per tick)
            totalTx += Math.floor(Math.random() * 50) + 10;
            // Format to have commas
            liveTotalTxEl.innerText = totalTx.toLocaleString('en-US');
        }, 80); // ticks every 80ms

        // Update TPS Fluctuations every second
        setInterval(() => {
            // Fluctuate roughly between 3.000 and 3.999
            const tps = 3000 + Math.floor(Math.random() * 999);
            // format to look like "3.xxx" (simulate European/Indonesian thousand separator)
            liveTpsEl.innerText = (tps / 1000).toFixed(3);
        }, 1000);


        // 2. Wave Canvas Animation
        const canvas = document.getElementById('waveCanvas');
        if(canvas) {
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
                
                const waves = [
                    { color: 'rgba(16, 185, 129, 0.3)', speed: 0.5, freq: 0.001, amp: 200 }, // Emerald
                    { color: 'rgba(14, 165, 233, 0.2)', speed: 0.8, freq: 0.002, amp: 180 }, // Sky blue
                    { color: 'rgba(139, 92, 246, 0.2)', speed: 1.2, freq: 0.0015, amp: 220 }  // Purple
                ];
                
                waves.forEach((wave, i) => {
                    ctx.beginPath();
                    ctx.moveTo(0, height / 2);
                    
                    for (let x = 0; x <= width; x += 10) {
                        let y = Math.sin((x * wave.freq) + (time * wave.speed) + i) * wave.amp * Math.sin(time + i);
                        y += Math.sin(x * 0.001 - time) * 80; 
                        ctx.lineTo(x, height / 2 + y);
                    }
                    
                    ctx.lineWidth = 3;
                    ctx.strokeStyle = wave.color;
                    ctx.shadowColor = wave.color;
                    ctx.shadowBlur = 10;
                    ctx.stroke();
                    ctx.shadowBlur = 0;
                });
                
                requestAnimationFrame(animate);
            }
            animate();
        }
    </script>
</body>
</html>
