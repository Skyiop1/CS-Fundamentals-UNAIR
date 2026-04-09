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
            gap: var(--space-lg);
            margin-top: var(--space-2xl);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        @media (min-width: 640px) {
            .role-grid { grid-template-columns: 1fr 1fr; }
        }
        .role-card {
            text-align: center;
            padding: var(--space-xl);
            cursor: pointer;
            text-decoration: none;
            color: var(--color-text-primary);
        }
        .role-card .icon-wrapper {
            width: 64px;
            height: 64px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto var(--space-md);
            color: white;
        }
        .role-card.buyer .icon-wrapper { background: var(--color-primary); }
        .role-card.owner .icon-wrapper { background: var(--color-secondary); }
        .role-card.verifier .icon-wrapper { background: transparent; border: 2px solid var(--color-primary); color: var(--color-primary); }
        .role-card.admin .icon-wrapper { background: transparent; border: 2px solid var(--color-text-muted); color: var(--color-text-secondary); }
    </style>
</head>
<body style="background: var(--gradient-hero); min-height: 100vh; display: flex; flex-direction: column;">
    
    <main class="container" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: var(--space-2xl) var(--space-md);">
        <div class="fade-up">
            <div class="logo-icon" style="width: 56px; height: 56px; margin: 0 auto var(--space-md);">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-leaf" width="32" height="32">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
                    <path d="M2 22 12 12"/>
                </svg>
            </div>
            <h1 style="font-size: var(--text-4xl); letter-spacing: -0.02em;">NusaCarbon</h1>
            <p class="text-lg text-muted" style="max-width: 600px; margin: 0 auto var(--space-xl);">Transparent. Verified. Tokenized Carbon Credits.</p>
            <p style="max-width: 600px; margin: 0 auto;">NusaCarbon adalah platform marketplace token kredit karbon berbasis blockchain untuk Indonesia, mengintegrasikan dMRV (digital Monitoring, Reporting & Verification) untuk memastikan setiap kredit yang ditokenisasi nyata, terukur, dan tercatat secara permanen.</p>
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
        
        <div class="fade-up" style="animation-delay: 200ms; margin-top: var(--space-2xl);">
            <a href="/buyer/marketplace.php" class="btn-outline">Explore Marketplace &rarr;</a>
        </div>
    </main>

    <footer style="text-align: center; padding: var(--space-xl) var(--space-md); color: var(--color-text-muted); font-size: var(--text-sm);">
        <p>&copy; 2026 NusaCarbon. All rights reserved.</p>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
