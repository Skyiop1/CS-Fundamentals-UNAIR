<?php
// owner/project-form.php
require_once '../includes/auth.php';
requireRole('owner');
require_once '../includes/db.php';

$stmt = $pdo->query("SELECT * FROM project_categories");
$categories = $stmt->fetchAll();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Process form
    $nama = $_POST['nama_project'];
    $kategori = $_POST['id_kategori'];
    $lokasi = $_POST['lokasi'];
    $luas = $_POST['luas_lahan'];
    $desc = $_POST['deskripsi'];

    $stmt = $pdo->prepare("INSERT INTO projects (id_user, id_kategori, nama_project, lokasi, luas_lahan, deskripsi, status_project) VALUES (?, ?, ?, ?, ?, ?, 'submitted')");
    $stmt->execute([$_SESSION['user_id'], $kategori, $nama, $lokasi, $luas, $desc]);
    
    header("Location: dashboard.php");
    exit;
}

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <div class="dashboard-header">
        <a href="dashboard.php" class="text-sm text-muted hover-primary" style="display: block; margin-bottom: var(--space-xs);">&larr; Kembali ke Dashboard</a>
        <h2 class="dashboard-title">Daftarkan Proyek Baru</h2>
        <p class="dashboard-subtitle">Lengkapi formulir untuk mengajukan registrasi proyek sertifikasi.</p>
    </div>

    <div class="card" style="max-width: 600px;">
        <form method="POST">
            <div class="form-group">
                <label>Nama Proyek</label>
                <input type="text" name="nama_project" class="form-control" required placeholder="Contoh: Konservasi Lahan Gambut X">
            </div>
            <div class="form-group">
                <label>Kategori Proyek</label>
                <select name="id_kategori" class="form-control" required>
                    <?php foreach($categories as $cat): ?>
                        <option value="<?= $cat['id_kategori'] ?>"><?= htmlspecialchars($cat['nama_kategori']) ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="form-group">
                <label>Lokasi (Provinsi/Pulau)</label>
                <input type="text" name="lokasi" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Luas Lahan (Ha)</label>
                <input type="number" step="0.01" name="luas_lahan" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Deskripsi Tujuan & Dampak</label>
                <textarea name="deskripsi" class="form-control" rows="4" required></textarea>
            </div>
            
            <hr style="border:0; border-top: 1px solid var(--color-border); margin: var(--space-lg) 0;">

            <h3>Dokumen Pendukung (Mock)</h3>
            <p class="text-xs text-muted" style="margin-bottom: var(--space-md);">Sistem saat ini otomatis menganggap dokumen valid untuk simulasi.</p>
            <div class="form-group">
                <label>Surat Keterangan Lahan & Izin (PDF)</label>
                <input type="file" class="form-control" style="padding: 6px;">
            </div>

            <button type="submit" class="btn-primary btn-full" style="padding: 12px; margin-top: var(--space-lg);">Submit Proyek ke Verifikator</button>
        </form>
    </div>
</div>

<?php require_once '../includes/footer.php'; ?>
