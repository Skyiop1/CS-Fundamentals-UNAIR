<?php
// login.php
session_start();
require_once 'includes/db.php';

// If already logged in, redirect
if (isset($_SESSION['user_id']) && isset($_SESSION['role'])) {
    $dest = ($_SESSION['role'] === 'buyer') ? '/buyer/home.php' : '/' . $_SESSION['role'] . '/dashboard.php';
    header("Location: $dest");
    exit;
}

$role = $_GET['role'] ?? '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email    = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $role_input = $_POST['role'] ?? '';

    // Build query — if role is provided, filter by it; otherwise just match email
    if (!empty($role_input)) {
        $stmt = $pdo->prepare("
            SELECT u.*, r.role_name 
            FROM users u
            JOIN roles r ON u.id_role = r.id_role
            WHERE u.email = ? AND r.role_name = ?
        ");
        $stmt->execute([$email, $role_input]);
    } else {
        $stmt = $pdo->prepare("
            SELECT u.*, r.role_name 
            FROM users u
            JOIN roles r ON u.id_role = r.id_role
            WHERE u.email = ?
        ");
        $stmt->execute([$email]);
    }

    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id']   = $user['id_user'];
        $_SESSION['role']      = $user['role_name'];
        $_SESSION['user_name'] = $user['nama_user'];
        $_SESSION['kyc']       = $user['status_kyc'];

        $redirect = $_GET['redirect'] ?? null;
        if ($redirect) {
            header("Location: $redirect");
        } elseif ($user['role_name'] === 'buyer') {
            header("Location: /buyer/home.php");
        } else {
            header("Location: /" . $user['role_name'] . "/dashboard.php");
        }
        exit;
    } else {
        $error = 'Email atau password salah.';
    }
}

// Fetch roles for dropdown (for users coming without ?role param)
$roles_list = $pdo->query("SELECT * FROM roles")->fetchAll();
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - NusaCarbon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        body, html {
            margin: 0; padding: 0; box-sizing: border-box; 
            width: 100%; height: 100vh; overflow: hidden;
            font-family: 'Inter', sans-serif;
            background: #02120b; /* Match index.php dark mode teal hint */
        }
        .split-layout {
            display: flex; height: 100%; width: 100%;
        }
        
        /* LEFT PANE: Animated Video Background */
        .left-pane {
            flex: 1; position: relative; 
            display: flex; flex-direction: column; justify-content: center; 
            padding: 8%; color: white;
            background: radial-gradient(circle at 30% 70%, #064e3b 0%, #02120b 70%); /* Deep emerald glow */
            overflow: hidden;
        }
        #waveCanvas {
            position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; mix-blend-mode: screen; opacity: 0.8;
            pointer-events: none;
        }
        .left-content {
            position: relative; z-index: 10; max-width: 650px;
        }
        .brand-logo {
            display: flex; align-items: center; gap: 12px; margin-bottom: 80px;
            font-size: 1.5rem; font-weight: 700; letter-spacing: -1px;
        }
        .left-content h1 {
            font-size: 4.5rem; line-height: 1.1; letter-spacing: -2px; 
            margin-bottom: 30px; font-weight: 800;
            background: linear-gradient(to right, #ffffff, #a1a1aa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .left-content p {
            font-size: 1.25rem; color: #a1a1aa; line-height: 1.6; max-width: 500px;
        }

        /* RIGHT PANE: Login Form */
        .right-pane {
            width: 480px; background: #09090b; 
            display: flex; flex-direction: column; justify-content: center; 
            padding: 60px; border-left: 1px solid rgba(255,255,255,0.05);
            color: #ffffff;
        }
        .auth-form-container { width: 100%; max-width: 360px; margin: 0 auto; }
        .right-pane h2 { font-size: 1.75rem; font-weight: 700; margin-bottom: 8px; color: #ffffff !important; }
        .right-pane p.subtitle { color: #a1a1aa; font-size: 0.95rem; margin-bottom: 32px; } 
        
        .right-pane .form-control {
            background: #18181b; border: 1px solid #27272a; color: white;
            padding: 14px 16px; border-radius: 12px; transition: 0.3s;
        }
        .right-pane .form-control:focus {
            border-color: #10b981; box-shadow: 0 0 0 2px rgba(16,185,129,0.2);
        }
        .right-pane label { color: #d4d4d8; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; display: block; }
        .right-pane .form-group { margin-bottom: 20px; }
        
        .btn-submit {
            background: #10b981; color: white; width: 100%; padding: 14px; 
            border: none; border-radius: 12px; font-weight: 600; font-size: 1rem;
            cursor: pointer; transition: 0.3s; margin-top: 10px;
        }
        .btn-submit:hover { background: #059669; transform: translateY(-2px); }

        @media (max-width: 900px) {
            .split-layout { flex-direction: column; }
            .left-pane { display: none; } /* Hide visual on mobile */
            .right-pane { width: 100%; height: 100vh; padding: 30px; border-left: none; }
        }
    </style>
</head>
<body>
    
    <div class="split-layout">
        <!-- VIDEO / ANIMATION PANE -->
        <div class="left-pane">
            <canvas id="waveCanvas"></canvas>
            <div class="left-content fade-up">
                <div class="brand-logo">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="28" height="28">
                        <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 22 12 12"/>
                    </svg>
                    NusaCarbon
                </div>
                <h1>Bursa karbon <br>untuk masa depan<br>bumi kita.</h1>
                <p>Jaringan berkinerja tinggi yang mendesentralisasi verifikasi proyek dMRV dan mendukung perdagangan kredit iklim transparan.</p>
            </div>
        </div>

        <!-- AUTH PANE -->
        <div class="right-pane">
            <div class="auth-form-container fade-up" style="animation-delay: 100ms;">
                <h2>Selamat Datang</h2>
                <?php if ($role): ?>
                    <p class="subtitle">Masuk sebagai <strong style="color: #10b981; text-transform: capitalize;"><?= htmlspecialchars($role) ?></strong></p>
                <?php else: ?>
                    <p class="subtitle">Masuk ke platform ekosistem NusaCarbon.</p>
                <?php endif; ?>

                <?php if ($error): ?>
                    <div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); padding: 12px; border-radius: 8px; margin-bottom: 24px; font-size: 14px; display: flex; align-items: center; gap: 8px;">
                        <i data-lucide="alert-circle" width="16"></i> <?= htmlspecialchars($error) ?>
                    </div>
                <?php endif; ?>

                <form method="POST">
                    <div class="form-group">
                        <label>Alamat Email</label>
                        <input type="email" name="email" class="form-control" required placeholder="nama@perusahaan.com" value="<?= htmlspecialchars($_POST['email'] ?? ($role ? $role . '@nusacarbon.id' : '')) ?>">
                    </div>
                    
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" name="password" class="form-control" required placeholder="••••••••">
                    </div>

                    <?php if ($role): ?>
                        <input type="hidden" name="role" value="<?= htmlspecialchars($role) ?>">
                    <?php else: ?>
                        <div class="form-group">
                            <label>Role</label>
                            <select name="role" class="form-control" style="appearance: none;">
                                <option value="">Auto-detect dari email</option>
                                <?php foreach ($roles_list as $r): ?>
                                    <option value="<?= htmlspecialchars($r['role_name']) ?>"><?= ucfirst(htmlspecialchars($r['role_name'])) ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    <?php endif; ?>
                    
                    <button type="submit" class="btn-submit">Masuk ke Dashboard</button>
                </form>

                <div style="text-align: center; margin-top: 40px; font-size: 0.85rem; color: #a1a1aa;">
                    Belum punya akun? <a href="/register.php" style="color: #10b981; text-decoration: none; font-weight: 500;">Daftar Mandiri</a><br>
                    <a href="/" style="display: inline-block; margin-top: 16px; color: #71717a; text-decoration: none;">&larr; Kembali ke Beranda</a>
                </div>
            </div>
        </div>
    </div>

    <!-- SCRIPT ANIMASI VIDEO (CANVAS) -->
    <script>
    lucide.createIcons();

    const canvas = document.getElementById('waveCanvas');
    if(canvas) {
        const ctx = canvas.getContext('2d');
        let width, height;
        let time = 0;

        function resize() {
            width = canvas.parentElement.clientWidth;
            height = canvas.parentElement.clientHeight;
            // Gunakan pixel ratio ganda agar tajam (HD)
            canvas.width = width * 2;
            canvas.height = height * 2;
            ctx.scale(2, 2);
        }
        window.addEventListener('resize', resize);
        resize();

        function animate() {
            ctx.clearRect(0, 0, width, height);
            time += 0.005; 
            
            // 3 Lapisan Garis Neons (seperti Solana)
            const waves = [
                { color: 'rgba(16, 185, 129, 0.4)', speed: 0.5, freq: 0.002, amp: 100 },
                { color: 'rgba(56, 189, 248, 0.4)', speed: 0.8, freq: 0.003, amp: 140 },
                { color: 'rgba(139, 92, 246, 0.5)', speed: 1.2, freq: 0.001, amp: 180 }
            ];
            
            waves.forEach((wave, i) => {
                ctx.beginPath();
                ctx.moveTo(0, height / 2);
                
                for (let x = 0; x <= width; x += 5) {
                    // Matematika gelombang harmonik ala Ticker Saham / Blockchain Flow
                    let y = Math.sin(x * wave.freq + time * wave.speed) * wave.amp * Math.sin(time + i);
                    y += Math.sin(x * 0.001 - time) * 50; 
                    ctx.lineTo(x, height / 2 + y);
                }
                
                ctx.lineWidth = 4;
                ctx.strokeStyle = wave.color;
                // Soft glow
                ctx.shadowColor = wave.color;
                ctx.shadowBlur = 15;
                ctx.stroke();
                ctx.shadowBlur = 0; // reset
            });
            
            requestAnimationFrame(animate);
        }
        animate();
    }
    </script>
</body>
</html>
