<?php
// buyer/token-detail.php
require_once '../includes/auth.php';
requireRole('buyer');

require_once '../includes/db.php';
require_once '../includes/helpers.php';
require_once '../includes/blockchain.php';

$id_token = $_GET['id'] ?? null;
if (!$id_token) { header("Location: tokens.php"); exit; }

$stmt = $pdo->prepare("
    SELECT ct.*, p.nama_project, p.lokasi, p.deskripsi, pc.nama_kategori
    FROM carbon_tokens ct
    JOIN projects p ON ct.id_project = p.id_project
    JOIN project_categories pc ON p.id_kategori = pc.id_kategori
    WHERE ct.id_token = ? AND ct.owner_user_id = ?
");
$stmt->execute([$id_token, $_SESSION['user_id']]);
$token = $stmt->fetch();

if (!$token) { die("Token tidak ditemukan atau bukan milik Anda."); }

// Blockchain trail for this token's project
$stmt = $pdo->prepare("SELECT * FROM blockchain_ledger WHERE ref_id = ? OR ref_table = 'carbon_tokens' ORDER BY id ASC");
$stmt->execute([$id_token]);
$ledger = $stmt->fetchAll();

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <a href="tokens.php" class="text-sm text-muted" style="display: block; margin-bottom: var(--space-md);">&larr; Kembali ke Token Saya</a>

    <div class="split-layout">
        <!-- Left: Token Details -->
        <div>
            <div class="card" style="margin-bottom: var(--space-lg);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--space-lg);">
                    <div>
                        <h2 style="margin-bottom: var(--space-xs);">Detail Token</h2>
                        <p class="text-muted text-sm"><?= htmlspecialchars($token['nama_project']) ?></p>
                    </div>
                    <?php
                    $badge = match($token['status_token']) {
                        'available', 'sold' => '<span class="badge badge--verified" style="font-size: var(--text-sm); padding: 6px 14px;">✓ Aktif</span>',
                        'retired' => '<span class="badge badge--rejected" style="font-size: var(--text-sm); padding: 6px 14px;">🔥 Retired</span>',
                        default => '<span class="badge badge--pending" style="font-size: var(--text-sm); padding: 6px 14px;">⏳ Pending</span>',
                    };
                    echo $badge;
                    ?>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-lg);">
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Token Serial</p>
                        <div class="hash-display" style="margin-top: 4px; font-size: var(--text-sm);">
                            <?= htmlspecialchars($token['token_serial']) ?>
                            <button class="hash-btn" onclick="copyToClipboard('<?= $token['token_serial'] ?>')"><i data-lucide="copy" width="12"></i></button>
                        </div>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Vintage Year</p>
                        <p style="font-weight: 600; margin: 4px 0 0;"><?= $token['vintage_year'] ?></p>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Kategori</p>
                        <span class="badge badge-cat-<?= strtolower(strtok($token['nama_kategori'], " ")) ?>" style="margin-top: 4px;">
                            <?= htmlspecialchars($token['nama_kategori']) ?>
                        </span>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Lokasi</p>
                        <p style="margin: 4px 0 0; display: flex; align-items: center; gap: 4px;"><i data-lucide="map-pin" width="14"></i> <?= htmlspecialchars($token['lokasi']) ?></p>
                    </div>
                </div>

                <hr style="border: 0; border-top: 1px solid var(--color-border); margin: var(--space-xl) 0;">

                <h3>Blockchain Hashes</h3>
                <div style="display: grid; grid-template-columns: 1fr; gap: var(--space-md); background: var(--color-bg); padding: var(--space-md); border-radius: var(--radius-md);">
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Tx Mint Hash</p>
                        <div class="hash-display" style="margin-top: 4px;">
                            <?= $token['tx_mint_hash'] ? truncateHash($token['tx_mint_hash']) : '—' ?>
                            <?php if ($token['tx_mint_hash']): ?>
                                <button class="hash-btn" onclick="copyToClipboard('<?= $token['tx_mint_hash'] ?>')"><i data-lucide="copy" width="12"></i></button>
                            <?php endif; ?>
                        </div>
                    </div>
                    <div>
                        <p class="text-xs text-muted" style="margin: 0;">Metadata Hash</p>
                        <div class="hash-display" style="margin-top: 4px;">
                            <?= $token['metadata_hash'] ? truncateHash($token['metadata_hash']) : '—' ?>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Blockchain Provenance Trail -->
            <div class="card">
                <h3>Blockchain Provenance Trail</h3>
                <p class="text-sm text-muted" style="margin-bottom: var(--space-md);">Riwayat transaksi on-chain (append-only ledger)</p>
                <?php if (empty($ledger)): ?>
                    <p class="text-muted" style="text-align: center; padding: var(--space-lg);">Belum ada entri blockchain untuk token ini.</p>
                <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Block</th>
                                <th>Tipe</th>
                                <th>Amount</th>
                                <th>Tx Hash</th>
                                <th>Tanggal</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($ledger as $entry): ?>
                            <tr>
                                <td style="font-weight: 600;">#<?= $entry['block_number'] ?></td>
                                <td>
                                    <?php
                                    $typeBadge = match($entry['tx_type']) {
                                        'mint' => '<span class="badge badge--verified">Mint</span>',
                                        'transfer' => '<span class="badge badge--transfer">Transfer</span>',
                                        'retire' => '<span class="badge badge--rejected">Retire</span>',
                                    };
                                    echo $typeBadge;
                                    ?>
                                </td>
                                <td><?= formatCO2e($entry['amount_co2e']) ?></td>
                                <td>
                                    <span class="hash-display">
                                        <?= truncateHash($entry['tx_hash']) ?>
                                        <button class="hash-btn" onclick="copyToClipboard('<?= $entry['tx_hash'] ?>')"><i data-lucide="copy" width="12"></i></button>
                                    </span>
                                </td>
                                <td class="text-sm text-muted"><?= formatDate($entry['created_at']) ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Right: Actions -->
        <div style="position: sticky; top: 90px;">
            <?php if (in_array($token['status_token'], ['available', 'sold'])): ?>
            <div class="card" style="text-align: center;">
                <div style="margin-bottom: var(--space-md);">
                    <i data-lucide="flame" width="32" height="32" style="color: var(--color-rejected);"></i>
                </div>
                <h3>Retire Token Ini</h3>
                <p class="text-sm text-muted">Retirement menghapus token dari sirkulasi secara permanen — mencegah double offset claim.</p>
                <a href="retire.php?id=<?= $token['id_token'] ?>" class="btn-primary btn-full" style="margin-top: var(--space-md); background: var(--color-rejected);">
                    Retire Token
                </a>
                <p class="text-xs text-muted" style="margin-top: var(--space-sm);">⚠️ Tindakan ini tidak dapat dibatalkan.</p>
            </div>
            <?php else: ?>
            <div class="card" style="text-align: center; background: var(--color-bg);">
                <i data-lucide="check-circle" width="32" height="32" style="color: var(--color-text-muted);"></i>
                <p class="text-muted" style="margin-top: var(--space-sm);">Token ini sudah di-retire dan tidak dapat digunakan kembali.</p>
                <a href="certificate.php" class="btn-outline" style="margin-top: var(--space-md);">Lihat Sertifikat</a>
            </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php require_once '../includes/footer.php'; ?>
