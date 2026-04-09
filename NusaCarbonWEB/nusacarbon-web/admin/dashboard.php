<?php
// admin/dashboard.php
require_once '../includes/auth.php';
requireRole('admin');

require_once '../includes/db.php';
require_once '../includes/helpers.php';

// Proses aksi persetujuan/penolakan KYC
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['user_id'], $_POST['action'])) {
    $target_user_id = (int) $_POST['user_id'];
    $new_status = ($_POST['action'] === 'approve') ? 'verified' : 'rejected';
    
    $stmt_update = $pdo->prepare("UPDATE users SET status_kyc = ? WHERE id_user = ?");
    $stmt_update->execute([$new_status, $target_user_id]);
    
    // Redirect untuk menghindari re-submission saat refresh
    header("Location: dashboard.php");
    exit;
}

// Example overview count
$stmt_users = $pdo->query("SELECT COUNT(*) FROM users");
$total_users = $stmt_users->fetchColumn();

// KYC Queue
$stmt_kyc = $pdo->query("SELECT * FROM users WHERE status_kyc = 'pending' ORDER BY created_at ASC");
$kyc_queue = $stmt_kyc->fetchAll();

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <div class="dashboard-header">
        <div>
            <h2 class="dashboard-title">Dashboard Administrator</h2>
            <p class="dashboard-subtitle">Monitor Platform & KYC Management</p>
        </div>
    </div>

    <div class="stats-grid">
        <div class="card">
            <p class="metric-label">Total Pengguna</p>
            <p class="metric-value"><?= $total_users ?></p>
        </div>
        <div class="card">
            <p class="metric-label">KYC Pending</p>
            <p class="metric-value" style="color: var(--color-pending);"><?= count($kyc_queue) ?></p>
        </div>
        <div class="card">
            <p class="metric-label">Proyek Aktif (Verifikasi)</p>
            <p class="metric-value" style="color: var(--color-verified);">4</p>
        </div>
        <div class="card">
            <p class="metric-label">Total Token Beredar</p>
            <p class="metric-value">45.000 <span class="text-sm">tCO₂e</span></p>
        </div>
    </div>

    <h3>Customer Due Diligence (KYC) Queue</h3>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Nama</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Tanggal Daftar</th>
                    <th>Status</th>
                    <th>Aksi</th>
                </tr>
            </thead>
            <tbody>
                <?php if (empty($kyc_queue)): ?>
                <tr><td colspan="6" style="text-align: center;">Tidak ada antrian KYC. Semua pengguna sudah diverifikasi.</td></tr>
                <?php endif; ?>

                <?php foreach($kyc_queue as $u): ?>
                <tr>
                    <td style="font-weight: 500;"><?= htmlspecialchars($u['nama_user']) ?></td>
                    <td><?= htmlspecialchars($u['email']) ?></td>
                    <td><span class="badge badge-cat-energi"><?= htmlspecialchars($u['id_role']) ?></span></td>
                    <td class="text-sm"><?= formatDate($u['created_at']) ?></td>
                    <td><span class="badge badge--pending">Pending</span></td>
                    <td>
                        <form method="POST" style="display: flex; gap: 8px; margin: 0;">
                            <input type="hidden" name="user_id" value="<?= $u['id_user'] ?>">
                            <button type="submit" name="action" value="approve" class="btn-primary btn-sm" onclick="return confirm('Yakin ingin menyetujui user ini?');"><i data-lucide="check-circle" width="14"></i> Approve</button>
                            <button type="submit" name="action" value="reject" class="btn-outline btn-sm" style="color: var(--color-rejected); border-color: var(--color-rejected);" onclick="return confirm('Tolak verifikasi user ini?');"><i data-lucide="x-circle" width="14"></i> Reject</button>
                        </form>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>

<?php require_once '../includes/footer.php'; ?>
