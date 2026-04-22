<?php
// buyer/tokens.php
require_once '../includes/auth.php';
requireRole('buyer');

require_once '../includes/db.php';
require_once '../includes/helpers.php';

// Fetch tokens owned by this user
$stmt = $pdo->prepare("
    SELECT ct.*, p.nama_project, p.lokasi, pc.nama_kategori
    FROM carbon_tokens ct
    JOIN projects p ON ct.id_project = p.id_project
    JOIN project_categories pc ON p.id_kategori = pc.id_kategori
    WHERE ct.owner_user_id = ?
    ORDER BY ct.created_at DESC
");
$stmt->execute([$_SESSION['user_id']]);
$tokens = $stmt->fetchAll();

// Count by status
$count_all     = count($tokens);
$count_active  = 0;
$count_retired = 0;
$count_pending = 0;
foreach ($tokens as $t) {
    if ($t['status_token'] === 'sold') $count_active++;
    elseif ($t['status_token'] === 'retired') $count_retired++;
    elseif ($t['status_token'] === 'listed') $count_pending++;
}

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <div class="dashboard-header">
        <div>
            <h2 class="dashboard-title">Token Saya</h2>
            <p class="dashboard-subtitle">Kelola carbon credit token milik Anda</p>
        </div>
        <div class="quick-actions">
            <a href="marketplace.php" class="btn-primary"><i data-lucide="plus-circle" width="16"></i> Beli Token Baru</a>
        </div>
    </div>

    <!-- Stats Row -->
    <div class="stats-grid" style="grid-template-columns: repeat(2, 1fr);">
        <div class="card">
            <p class="metric-label">Total Token Dimiliki</p>
            <p class="metric-value" style="color: var(--color-primary);"><?= formatCO2e($count_all) ?></p>
        </div>
        <div class="card">
            <p class="metric-label">Proyek Aktif</p>
            <p class="metric-value"><?= $count_active ?> <span class="text-sm text-muted">(+<?= $count_pending ?> pending)</span></p>
        </div>
    </div>

    <!-- Tabs -->
    <div class="tabs-container">
        <div class="tabs-header">
            <button class="tab-btn active" data-tab="tab-semua">Semua (<?= $count_all ?>)</button>
            <button class="tab-btn" data-tab="tab-aktif">Aktif (<?= $count_active ?>)</button>
            <button class="tab-btn" data-tab="tab-retired">Retired (<?= $count_retired ?>)</button>
            <button class="tab-btn" data-tab="tab-pending">Pending (<?= $count_pending ?>)</button>
        </div>

        <!-- Tab: Semua -->
        <div class="tab-panel" id="tab-semua">
            <?php if (empty($tokens)): ?>
                <div class="card" style="text-align: center; padding: var(--space-2xl);">
                    <div style="margin-bottom: var(--space-md);">
                        <i data-lucide="inbox" width="48" height="48" style="color: var(--color-text-muted);"></i>
                    </div>
                    <h3 style="color: var(--color-text-muted);">Belum Ada Token</h3>
                    <p class="text-muted">Anda belum memiliki token kredit karbon. Mulai beli di marketplace.</p>
                    <a href="marketplace.php" class="btn-primary" style="margin-top: var(--space-md);">Jelajahi Marketplace</a>
                </div>
            <?php else: ?>
                <?php echo renderTokenTable($tokens, 'all'); ?>
            <?php endif; ?>
        </div>

        <!-- Tab: Aktif -->
        <div class="tab-panel hidden" id="tab-aktif">
            <?php
            $active = array_filter($tokens, fn($t) => $t['status_token'] === 'sold');
            if (empty($active)): ?>
                <div class="card" style="text-align: center; padding: var(--space-xl);"><p class="text-muted">Tidak ada token aktif.</p></div>
            <?php else: echo renderTokenTable($active, 'active'); endif; ?>
        </div>

        <!-- Tab: Retired -->
        <div class="tab-panel hidden" id="tab-retired">
            <?php
            $retired = array_filter($tokens, fn($t) => $t['status_token'] === 'retired');
            if (empty($retired)): ?>
                <div class="card" style="text-align: center; padding: var(--space-xl);"><p class="text-muted">Tidak ada token yang sudah di-retire.</p></div>
            <?php else: echo renderTokenTable($retired, 'retired'); endif; ?>
        </div>

        <!-- Tab: Pending -->
        <div class="tab-panel hidden" id="tab-pending">
            <?php
            $pending = array_filter($tokens, fn($t) => $t['status_token'] === 'listed');
            if (empty($pending)): ?>
                <div class="card" style="text-align: center; padding: var(--space-xl);"><p class="text-muted">Tidak ada token pending.</p></div>
            <?php else: echo renderTokenTable($pending, 'pending'); endif; ?>
        </div>
    </div>
</div>

<?php
function renderTokenTable(array $tokens, string $context): string {
    $html = '<div class="table-responsive" style="margin-top: var(--space-md);">
        <table class="table">
            <thead>
                <tr>
                    <th>Token Serial</th>
                    <th>Proyek</th>
                    <th>Kategori</th>
                    <th>Lokasi</th>
                    <th>Vintage</th>
                    <th>Status</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>';
    
    foreach ($tokens as $t) {
        $badge = match($t['status_token']) {
            'sold' => '<span class="badge badge--verified">✓ Aktif</span>',
            'retired' => '<span class="badge badge--rejected">🔥 Retired</span>',
            'listed'  => '<span class="badge badge--pending">⏳ Pending</span>',
            default   => '<span class="badge badge--dark">' . $t['status_token'] . '</span>',
        };

        $serial = '<span class="hash-display">' . htmlspecialchars($t['token_serial']) . '</span>';
        $actions = '<a href="token-detail.php?id=' . $t['id_token'] . '" class="btn-outline btn-sm">Detail</a>';
        if ($t['status_token'] === 'sold') {
            $actions .= ' <a href="retire.php?id=' . $t['id_token'] . '" class="btn-outline btn-sm" style="color: var(--color-rejected); border-color: var(--color-rejected);">Retire</a>';
        }

        $html .= '<tr>
            <td>' . $serial . '</td>
            <td style="font-weight: 500;">' . htmlspecialchars($t['nama_project']) . '</td>
            <td><span class="badge badge-cat-' . strtolower(strtok($t['nama_kategori'], " ")) . '">' . htmlspecialchars($t['nama_kategori']) . '</span></td>
            <td class="text-muted text-sm"><i data-lucide="map-pin" width="12"></i> ' . htmlspecialchars($t['lokasi']) . '</td>
            <td>' . $t['vintage_year'] . '</td>
            <td>' . $badge . '</td>
            <td>' . $actions . '</td>
        </tr>';
    }
    
    $html .= '</tbody></table></div>';
    return $html;
}
?>

<?php require_once '../includes/footer.php'; ?>
