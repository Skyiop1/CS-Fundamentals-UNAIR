<?php
// buyer/certificate.php
require_once '../includes/auth.php';
requireRole('buyer');

require_once '../includes/db.php';
require_once '../includes/helpers.php';

// Fetch all certificates for this user
$stmt = $pdo->prepare("
    SELECT c.*, r.tx_retirement_hash, r.created_at as retire_date
    FROM certificates c
    JOIN retirements r ON c.id_retirement = r.id_retirement
    WHERE r.id_user = ?
    ORDER BY c.created_at DESC
");
$stmt->execute([$_SESSION['user_id']]);
$certificates = $stmt->fetchAll();

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <div class="dashboard-header">
        <div>
            <h2 class="dashboard-title">Sertifikat Karbon Offset</h2>
            <p class="dashboard-subtitle">Bukti retirement token kredit karbon Anda</p>
        </div>
    </div>

    <?php if (empty($certificates)): ?>
    <div class="card" style="text-align: center; padding: var(--space-2xl);">
        <div style="margin-bottom: var(--space-md);">
            <i data-lucide="award" width="48" height="48" style="color: var(--color-text-muted);"></i>
        </div>
        <h3 style="color: var(--color-text-muted);">Belum Ada Sertifikat</h3>
        <p class="text-muted">Anda belum memiliki sertifikat. Retire token Anda untuk mendapatkan sertifikat karbon offset.</p>
        <a href="tokens.php" class="btn-outline" style="margin-top: var(--space-md);">Lihat Token Saya</a>
    </div>
    <?php else: ?>

    <div style="display: grid; grid-template-columns: 1fr; gap: var(--space-lg);">
        <?php foreach ($certificates as $cert): ?>
        <div class="card" style="border-left: 4px solid var(--color-primary); position: relative; overflow: hidden;">
            <!-- Decorative watermark -->
            <div style="position: absolute; top: -20px; right: -20px; width: 120px; height: 120px; background: var(--gradient-primary); filter: blur(40px); opacity: 0.08;"></div>
            
            <div style="position: relative; z-index: 1;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: var(--space-md);">
                    <div>
                        <p class="text-xs text-muted" style="margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">Carbon Offset Certificate</p>
                        <h3 style="color: var(--color-primary); margin: 4px 0; font-size: var(--text-xl);"><?= htmlspecialchars($cert['nomor_sertifikat']) ?></h3>
                    </div>
                    <span class="badge badge--verified" style="font-size: var(--text-sm); padding: 6px 14px;">
                        <i data-lucide="shield-check" width="14"></i> Verified
                    </span>
                </div>

                <hr style="border: 0; border-top: 1px dashed var(--color-border); margin: var(--space-lg) 0;">

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: var(--space-lg);">
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Nama Entitas</p>
                        <p style="font-weight: 600; margin: 4px 0 0;"><?= htmlspecialchars($cert['nama_entitas']) ?></p>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Volume CO₂ Offset</p>
                        <p style="font-weight: 700; color: var(--color-primary); margin: 4px 0 0; font-size: var(--text-lg);"><?= formatCO2e($cert['total_co2e']) ?></p>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Tanggal Retirement</p>
                        <p style="margin: 4px 0 0;"><?= formatDate($cert['retire_date']) ?></p>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Tx Retirement Hash</p>
                        <div class="hash-display" style="margin-top: 4px;">
                            <?= $cert['tx_retirement_hash'] ? truncateHash($cert['tx_retirement_hash']) : '—' ?>
                            <?php if ($cert['tx_retirement_hash']): ?>
                            <button class="hash-btn" onclick="copyToClipboard('<?= $cert['tx_retirement_hash'] ?>')"><i data-lucide="copy" width="12"></i></button>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>

                <div style="margin-top: var(--space-xl); display: flex; gap: var(--space-md);">
                    <button class="btn-primary btn-sm" onclick="showToast('Download PDF certificate (mock)', 'info')">
                        <i data-lucide="download" width="14"></i> Download PDF
                    </button>
                    <button class="btn-outline btn-sm" onclick="showToast('Share certificate link copied!', 'success')">
                        <i data-lucide="share-2" width="14"></i> Share
                    </button>
                </div>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
    <?php endif; ?>
</div>

<?php require_once '../includes/footer.php'; ?>
