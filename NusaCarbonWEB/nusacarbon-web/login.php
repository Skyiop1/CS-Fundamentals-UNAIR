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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <link rel="stylesheet" href="/assets/css/dashboard.css">
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
</head>
<body class="auth-layout">
    
    <div class="card auth-card fade-up">
        <div style="text-align: center; margin-bottom: var(--space-xl);">
            <div class="logo-icon" style="margin: 0 auto var(--space-sm);">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
                    <path d="M2 22 12 12"/>
                </svg>
            </div>
            <h2 style="margin-bottom: var(--space-xs);">Selamat Datang</h2>
            <?php if ($role): ?>
                <p class="text-sm text-muted">Masuk sebagai <strong style="text-transform: capitalize; color: var(--color-primary);"><?= htmlspecialchars($role) ?></strong></p>
            <?php else: ?>
                <p class="text-sm text-muted">Masuk ke akun NusaCarbon Anda.</p>
            <?php endif; ?>
        </div>

        <?php if ($error): ?>
            <div style="background: var(--color-rejected-bg); color: var(--color-rejected); padding: 10px 14px; border-radius: var(--radius-md); margin-bottom: var(--space-md); font-size: var(--text-sm); display: flex; align-items: center; gap: 8px;">
                <i data-lucide="alert-circle" width="16"></i>
                <?= htmlspecialchars($error) ?>
            </div>
        <?php endif; ?>

        <form method="POST">
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" name="email" class="form-control" required 
                       placeholder="email@nusacarbon.id"
                       value="<?= htmlspecialchars($_POST['email'] ?? ($role ? $role . '@nusacarbon.id' : '')) ?>">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" class="form-control" required placeholder="••••••••">
            </div>

            <?php if ($role): ?>
                <!-- Role comes from landing page selection — locked -->
                <input type="hidden" name="role" value="<?= htmlspecialchars($role) ?>">
            <?php else: ?>
                <!-- No role preselected — let user pick or auto-detect -->
                <div class="form-group">
                    <label>Role <span class="text-muted text-xs">(opsional jika akun sudah spesifik)</span></label>
                    <select name="role" class="form-control">
                        <option value="">Auto-detect dari email</option>
                        <?php foreach ($roles_list as $r): ?>
                            <option value="<?= htmlspecialchars($r['role_name']) ?>"><?= ucfirst(htmlspecialchars($r['role_name'])) ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
            <?php endif; ?>
            
            <button type="submit" class="btn-primary btn-full" style="margin-top: var(--space-md); padding: 12px;">Login</button>
        </form>

        <div style="text-align: center; margin-top: var(--space-lg); font-size: var(--text-sm); border-top: 1px solid var(--color-border); padding-top: var(--space-lg);">
            Belum punya akun? <a href="/register.php">Daftar di sini</a><br>
            <a href="/" style="display: inline-block; margin-top: var(--space-sm);" class="text-muted">&larr; Kembali ke Home</a>
        </div>
    </div>

    <script>lucide.createIcons();</script>
</body>
</html>
