<?php
// buyer/retire.php
require_once '../includes/auth.php';
requireRole('buyer');

require_once '../includes/db.php';
require_once '../includes/helpers.php';
require_once '../includes/blockchain.php';

$id_token = $_GET['id'] ?? null;
$success = false;
$result = null;

// If specific token
if ($id_token) {
    $stmt = $pdo->prepare("
        SELECT ct.*, p.nama_project 
        FROM carbon_tokens ct
        JOIN projects p ON ct.id_project = p.id_project
        WHERE ct.id_token = ? AND ct.owner_user_id = ? AND ct.status_token IN ('available','sold')
    ");
    $stmt->execute([$id_token, $_SESSION['user_id']]);
    $token = $stmt->fetch();

    if (!$token) { die("Token tidak ditemukan, bukan milik Anda, atau sudah di-retire."); }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nama_entitas = trim($_POST['nama_entitas'] ?? '');
    $token_id = (int)$_POST['id_token'];

    if (empty($nama_entitas)) { $nama_entitas = $_SESSION['user_name']; }

    try {
        $pdo->beginTransaction();

        // 1. Insert retirement
        $stmt = $pdo->prepare("INSERT INTO retirements (id_user, nama_entitas, total_co2e) VALUES (?, ?, 1)");
        $stmt->execute([$_SESSION['user_id'], $nama_entitas]);
        $id_retire = $pdo->lastInsertId();

        // 2. Insert retirement detail
        $pdo->prepare("INSERT INTO retirement_details (id_retirement, id_token) VALUES (?, ?)")->execute([$id_retire, $token_id]);

        // 3. Mark token as retired (PERMANENT)
        $pdo->prepare("UPDATE carbon_tokens SET status_token = 'retired' WHERE id_token = ?")->execute([$token_id]);

        // 4. Append to blockchain ledger
        $txHash = appendToLedger($pdo, 'retire', $id_retire, 'retirements', 1, '0xUserVault', '0x' . str_repeat('0', 40));
        $pdo->prepare("UPDATE retirements SET tx_retirement_hash = ? WHERE id_retirement = ?")->execute([$txHash, $id_retire]);

        // 5. Issue certificate
        $certNo = generateCertNumber(date('Y'), $id_retire);
        $pdo->prepare("INSERT INTO certificates (id_retirement, nomor_sertifikat, nama_entitas, total_co2e) VALUES (?, ?, ?, 1)")->execute([$id_retire, $certNo, $nama_entitas]);

        // 6. Update wallet balance
        $pdo->prepare("UPDATE wallets SET saldo_token = GREATEST(saldo_token - 1, 0) WHERE id_user = ?")->execute([$_SESSION['user_id']]);

        $pdo->commit();
        $success = true;
        $result = ['tx_hash' => $txHash, 'cert_no' => $certNo];

    } catch (Exception $e) {
        if ($pdo->inTransaction()) $pdo->rollBack();
        die("Error: " . $e->getMessage());
    }
}

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <a href="tokens.php" class="text-sm text-muted" style="display: block; margin-bottom: var(--space-md);">&larr; Kembali ke Token Saya</a>

    <?php if ($success): ?>
    <!-- Success State -->
    <div class="card" style="max-width: 560px; margin: 0 auto; text-align: center; padding: var(--space-2xl);">
        <div style="width: 64px; height: 64px; border-radius: var(--radius-full); background: var(--color-verified-bg); display: flex; align-items: center; justify-content: center; margin: 0 auto var(--space-lg);">
            <i data-lucide="check-circle" width="32" height="32" style="color: var(--color-verified);"></i>
        </div>
        <h2 style="color: var(--color-verified);">Token Berhasil Di-Retire!</h2>
        <p class="text-muted">Token telah dihapus dari sirkulasi secara permanen. Sertifikat offset karbon telah diterbitkan.</p>

        <div style="background: var(--color-bg); padding: var(--space-lg); border-radius: var(--radius-md); margin: var(--space-xl) 0; text-align: left;">
            <div style="margin-bottom: var(--space-md);">
                <p class="text-xs text-muted" style="margin: 0;">Transaction Hash</p>
                <div class="hash-display" style="margin-top: 4px; font-size: var(--text-sm);">
                    <?= truncateHash($result['tx_hash']) ?>
                    <button class="hash-btn" onclick="copyToClipboard('<?= $result['tx_hash'] ?>')"><i data-lucide="copy" width="14"></i></button>
                </div>
            </div>
            <div>
                <p class="text-xs text-muted" style="margin: 0;">Nomor Sertifikat</p>
                <p style="font-weight: 700; color: var(--color-primary); margin: 4px 0 0; font-size: var(--text-lg);"><?= $result['cert_no'] ?></p>
            </div>
        </div>

        <div style="display: flex; gap: var(--space-md); justify-content: center;">
            <a href="certificate.php" class="btn-primary"><i data-lucide="download" width="16"></i> Lihat Sertifikat</a>
            <a href="tokens.php" class="btn-outline">Kembali ke Token</a>
        </div>
    </div>

    <?php else: ?>
    <!-- Confirm Retirement -->
    <div class="card" style="max-width: 560px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: var(--space-xl);">
            <div style="width: 56px; height: 56px; border-radius: var(--radius-full); background: var(--color-rejected-bg); display: flex; align-items: center; justify-content: center; margin: 0 auto var(--space-md);">
                <i data-lucide="flame" width="28" height="28" style="color: var(--color-rejected);"></i>
            </div>
            <h2>Konfirmasi Retirement</h2>
            <p class="text-muted">Anda akan me-retire token kredit karbon secara <strong>permanen</strong>.</p>
        </div>

        <?php if (isset($token)): ?>
        <div style="background: var(--color-bg); padding: var(--space-md); border-radius: var(--radius-md); margin-bottom: var(--space-lg);">
            <p style="font-weight: 600; margin: 0 0 4px;"><?= htmlspecialchars($token['nama_project']) ?></p>
            <div class="hash-display"><?= htmlspecialchars($token['token_serial']) ?></div>
            <p class="text-xs text-muted" style="margin: var(--space-sm) 0 0;">1 tCO₂e • Vintage <?= $token['vintage_year'] ?></p>
        </div>
        <?php endif; ?>

        <form method="POST">
            <input type="hidden" name="id_token" value="<?= $id_token ?>">
            <div class="form-group">
                <label>Nama Entitas (untuk sertifikat)</label>
                <input type="text" name="nama_entitas" class="form-control" 
                       value="<?= htmlspecialchars($_SESSION['user_name']) ?>" 
                       placeholder="<?= htmlspecialchars($_SESSION['user_name']) ?>">
                <p class="text-xs text-muted" style="margin-top: 4px;">Nama ini akan tertera di sertifikat karbon offset Anda.</p>
            </div>

            <div style="background: var(--color-rejected-bg); padding: var(--space-md); border-radius: var(--radius-md); margin-bottom: var(--space-lg); font-size: var(--text-sm); color: var(--color-rejected);">
                <strong>⚠️ Peringatan:</strong> Retirement bersifat permanen dan tidak dapat dibatalkan. Token akan dihapus dari sirkulasi untuk mencegah double offset claim.
            </div>

            <div style="display: flex; gap: var(--space-md);">
                <a href="tokens.php" class="btn-outline" style="flex: 1; text-align: center;">Batal</a>
                <button type="submit" class="btn-primary" style="flex: 1; background: var(--color-rejected);">Konfirmasi Retire</button>
            </div>
        </form>
    </div>
    <?php endif; ?>
</div>

<?php require_once '../includes/footer.php'; ?>
