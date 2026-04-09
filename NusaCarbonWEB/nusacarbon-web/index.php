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
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <link rel="stylesheet" href="/assets/css/dashboard.css">
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        .role-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: var(--space-xl);
            margin-top: var(--space-2xl);
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        @media (min-width: 640px) {
            .role-grid { grid-template-columns: 1fr 1fr; }
        }
        .role-card {
            text-align: center;
            padding: var(--space-2xl) var(--space-xl);
            cursor: pointer;
            text-decoration: none;
            /* Premium Glassmorphism */
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            color: #ffffff !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .role-card:hover {
            transform: translateY(-8px);
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3) !important;
        }
        .role-card h3 {
            color: #ffffff !important;
            font-size: var(--text-xl);
            margin-bottom: var(--space-xs);
            font-weight: 600;
        }
        .role-card p {
            color: rgba(255, 255, 255, 0.7) !important;
        }
        .role-card .icon-wrapper {
            width: 72px;
            height: 72px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto var(--space-lg);
            color: white;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }
        .role-card.buyer .icon-wrapper { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
        .role-card.owner .icon-wrapper { background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); }
        .role-card.verifier .icon-wrapper { background: rgba(255, 255, 255, 0.1); border: 2px solid rgba(255,255,255,0.3); color: #a7f3d0; }
        .role-card.admin .icon-wrapper { background: rgba(255, 255, 255, 0.1); border: 2px solid rgba(255,255,255,0.3); color: #cbd5e1; }
        
        /* Typography overrides for dark background */
        .hero-title {
            font-size: 3.5rem; /* Fixed: forced absolute size */
            letter-spacing: -0.03em;
            color: #ffffff;
            font-weight: 800;
            text-shadow: 0 4px 20px rgba(0,0,0,0.15);
            margin-bottom: 12px;
            margin-top: 0;
        }
        .hero-subtitle {
            color: #6ee7b7; /* Bright mint for contrast */
            font-weight: 500;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-size: var(--text-sm);
            margin-bottom: var(--space-lg);
        }
        .hero-desc {
            color: rgba(255, 255, 255, 0.85);
            font-size: var(--text-lg);
            line-height: 1.6;
            max-width: 650px;
            margin: 0 auto;
        }
    </style>
</head>
<body style="background: var(--gradient-hero); min-height: 100vh; display: flex; flex-direction: column;">
    
    <main class="container" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 60px var(--space-md);">
        <div class="fade-up">
            <div class="logo-icon" style="width: 64px; height: 64px; margin: 0 auto var(--space-lg); background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 20px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.2);">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#6ee7b7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-leaf" width="36" height="36">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
                    <path d="M2 22 12 12"/>
                </svg>
            </div>
            <h1 class="hero-title">NusaCarbon</h1>
            <p class="hero-subtitle">Transparent. Verified. Tokenized Carbon Credits.</p>
            <p class="hero-desc">Platform marketplace token kredit karbon berbasis blockchain untuk Indonesia. Mengintegrasikan dMRV (digital Monitoring, Reporting & Verification) demi memastikan setiap kredit offset Anda nyata, terukur, dan permanen.</p>
        </div>

        <div class="role-grid fade-up" style="animation-delay: 100ms; width: 100%;">
            <a href="/login.php?role=buyer" class="card role-card buyer">
                <div class="icon-wrapper"><i data-lucide="wallet" width="32" height="32"></i></div>
                <h3>Buyer</h3>
                <p class="text-sm text-muted">Beli token kredit karbon untuk personal atau korporasi.</p>
            </a>
            <a href="/login.php?role=owner" class="card role-card owner">
                <div class="icon-wrapper"><i data-lucide="leaf" width="32" height="32"></i></div>
                <h3>Project Owner</h3>
                <p class="text-sm text-muted">Daftarkan proyek lingkungan dan terbitkan token.</p>
            </a>
            <a href="/login.php?role=verifier" class="card role-card verifier">
                <div class="icon-wrapper"><i data-lucide="shield-check" width="32" height="32"></i></div>
                <h3>Verifier</h3>
                <p class="text-sm text-muted">Audit proyek dan MRV sebagai pihak independen.</p>
            </a>
            <a href="/login.php?role=admin" class="card role-card admin">
                <div class="icon-wrapper"><i data-lucide="settings" width="32" height="32"></i></div>
                <h3>Admin</h3>
                <p class="text-sm text-muted">Kelola platform dan verifikasi pengguna (KYC).</p>
            </a>
        </div>
        
        <div class="fade-up" style="animation-delay: 200ms; margin-top: 40px; margin-bottom: 20px;">
            <a href="/buyer/marketplace.php" class="btn-primary" style="background: white !important; color: #059669 !important; border: none; padding: 14px 32px; font-weight: bold; font-size: 16px; border-radius: 50px; box-shadow: 0 4px 20px rgba(0,255,150,0.2);">Explore Marketplace &rarr;</a>
        </div>
    </main>

    <footer style="text-align: center; padding: var(--space-xl) var(--space-md); color: rgba(255,255,255,0.5); font-size: var(--text-sm);">
        <p>&copy; 2026 NusaCarbon. All rights reserved.</p>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
