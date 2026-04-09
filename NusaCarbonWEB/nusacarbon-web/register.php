<?php
// register.php
session_start();
require_once 'includes/db.php';
require_once 'includes/helpers.php';

$error = '';
$success = '';

// Fetch roles for dropdown
$stmt = $pdo->query("SELECT * FROM roles");
$roles = $stmt->fetchAll();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nama     = trim($_POST['nama_user'] ?? '');
    $email    = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $confirm  = $_POST['confirm_password'] ?? '';
    $no_hp    = trim($_POST['no_hp'] ?? '');
    $id_role  = (int)($_POST['id_role'] ?? 0);

    // Validation
    if (empty($nama) || empty($email) || empty($password) || $id_role <= 0) {
        $error = 'Semua field wajib diisi.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = 'Format email tidak valid.';
    } elseif (strlen($password) < 6) {
        $error = 'Password minimal 6 karakter.';
    } elseif ($password !== $confirm) {
        $error = 'Konfirmasi password tidak cocok.';
    } else {
        // Check if email already exists
        $stmt = $pdo->prepare("SELECT id_user FROM users WHERE email = ?");
        $stmt->execute([$email]);
        if ($stmt->fetch()) {
            $error = 'Email sudah terdaftar. Silakan gunakan email lain.';
        } else {
            // Hash password with bcrypt
            $hashedPassword = password_hash($password, PASSWORD_BCRYPT);

            // Insert user
            $stmt = $pdo->prepare("INSERT INTO users (nama_user, email, password, no_hp, status_kyc, id_role) VALUES (?, ?, ?, ?, 'pending', ?)");
            $stmt->execute([$nama, $email, $hashedPassword, $no_hp, $id_role]);
            $newUserId = $pdo->lastInsertId();

            // Create wallet for the new user
            $walletAddress = generateMockWalletAddress();
            $stmt = $pdo->prepare("INSERT INTO wallets (id_user, wallet_address, saldo_token) VALUES (?, ?, 0)");
            $stmt->execute([$newUserId, $walletAddress]);

            $success = 'Registrasi berhasil! Silakan login dengan akun Anda.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registrasi - NusaCarbon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <link rel="stylesheet" href="/assets/css/dashboard.css">
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
</head>
<body class="auth-layout">
    
    <div class="card auth-card fade-up" style="max-width: 480px;">
        <div style="text-align: center; margin-bottom: var(--space-xl);">
            <div class="logo-icon" style="margin: 0 auto var(--space-sm);">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
                    <path d="M2 22 12 12"/>
                </svg>
            </div>
            <h2 style="margin-bottom: var(--space-xs);">Buat Akun Baru</h2>
            <p class="text-sm text-muted">Bergabung dengan NusaCarbon dan mulai aksi iklim Anda.</p>
        </div>

        <?php if ($error): ?>
            <div style="background: var(--color-rejected-bg); color: var(--color-rejected); padding: 10px 14px; border-radius: var(--radius-md); margin-bottom: var(--space-md); font-size: var(--text-sm); display: flex; align-items: center; gap: 8px;">
                <i data-lucide="alert-circle" width="16"></i>
                <?= htmlspecialchars($error) ?>
            </div>
        <?php endif; ?>

        <?php if ($success): ?>
            <div style="background: var(--color-verified-bg); color: var(--color-verified); padding: 10px 14px; border-radius: var(--radius-md); margin-bottom: var(--space-md); font-size: var(--text-sm); display: flex; align-items: center; gap: 8px;">
                <i data-lucide="check-circle" width="16"></i>
                <?= htmlspecialchars($success) ?>
            </div>
            <div style="text-align: center; margin-top: var(--space-md);">
                <a href="/login.php" class="btn-primary" style="display: inline-flex;">Login Sekarang &rarr;</a>
            </div>
        <?php else: ?>
        <form method="POST" autocomplete="off">
            <div class="form-group">
                <label>Nama Lengkap / Nama Perusahaan</label>
                <input type="text" name="nama_user" class="form-control" required 
                       placeholder="Contoh: PT Hijau Indonesia" 
                       value="<?= htmlspecialchars($_POST['nama_user'] ?? '') ?>">
            </div>

            <div class="form-group">
                <label>Alamat Email</label>
                <input type="email" name="email" class="form-control" required 
                       placeholder="email@contoh.com"
                       value="<?= htmlspecialchars($_POST['email'] ?? '') ?>">
            </div>

            <div class="form-group">
                <label>Nomor Telepon (Opsional)</label>
                <input type="text" name="no_hp" class="form-control" 
                       placeholder="+62 812 xxxx xxxx"
                       value="<?= htmlspecialchars($_POST['no_hp'] ?? '') ?>">
            </div>

            <div class="form-group">
                <label>Pilih Peran / Role</label>
                <select name="id_role" class="form-control" required>
                    <option value="">— Pilih Role —</option>
                    <?php foreach ($roles as $r): ?>
                        <option value="<?= $r['id_role'] ?>" <?= (isset($_POST['id_role']) && $_POST['id_role'] == $r['id_role']) ? 'selected' : '' ?>>
                            <?= ucfirst(htmlspecialchars($r['role_name'])) ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md);">
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" class="form-control" required 
                           placeholder="Min. 6 karakter" minlength="6">
                </div>
                <div class="form-group">
                    <label>Konfirmasi Password</label>
                    <input type="password" name="confirm_password" class="form-control" required 
                           placeholder="Ulangi password">
                </div>
            </div>

            <button type="submit" class="btn-primary btn-full" style="margin-top: var(--space-md); padding: 12px;">
                Daftar Akun
            </button>
            
            <p class="text-xs text-muted" style="text-align: center; margin-top: var(--space-md);">
                Dengan mendaftar, Anda menyetujui bahwa platform ini adalah <strong>simulasi</strong> akademis.<br>
                Status KYC Anda akan menjadi <em>Pending</em> dan harus disetujui oleh Admin.
            </p>
        </form>
        <?php endif; ?>

        <div style="text-align: center; margin-top: var(--space-lg); font-size: var(--text-sm); border-top: 1px solid var(--color-border); padding-top: var(--space-lg);">
            Sudah punya akun? <a href="/login.php">Login di sini</a><br>
            <a href="/" style="display: inline-block; margin-top: var(--space-sm);" class="text-muted">&larr; Kembali ke Home</a>
        </div>
    </div>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
