<?php
// buyer/wallet.php
require_once '../includes/auth.php';
requireRole('buyer');

require_once '../includes/db.php';
require_once '../includes/helpers.php';
require_once '../includes/blockchain.php';

// Fetch wallet info
$stmt = $pdo->prepare("SELECT * FROM wallets WHERE id_user = ?");
$stmt->execute([$_SESSION['user_id']]);
$wallet = $stmt->fetch();

if (!$wallet) {
    // Scaffold dummy wallet for test purposes if it doesn't exist
    $wallet = [
        'wallet_address' => generateMockWalletAddress(),
        'saldo_token' => 0
    ];
}

// Transaction History Mock
$tx_history = [
    ['type' => 'Transfer (Beli)', 'project' => 'Mangrove Restoration Borneo', 'amount' => '+5.000 tCO₂e', 'hash' => generateTxHash(GENESIS_HASH, 'transfer', 5000, 1, '2025-01-01'), 'date' => '2025-01-15'],
    ['type' => 'Retire (Burn)', 'project' => 'Solar Farm Bali', 'amount' => '-1.000 tCO₂e', 'hash' => generateTxHash('prev', 'retire', 1000, 2, '2025-01-01'), 'date' => '2025-02-10'],
];

require_once '../includes/header.php';
?>

<div class="dashboard-layout fade-up">
    <div class="dashboard-header" style="margin-bottom: var(--space-lg);">
        <h2 class="dashboard-title">Digital Wallet</h2>
    </div>

    <!-- Premium Web3 Wallet Card -->
    <div class="card" style="background: linear-gradient(145deg, #0f172a 0%, #064e3b 100%); color: white; margin-bottom: var(--space-xl); position: relative; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.1); padding: 40px; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.2);">
        
        <!-- Glowing Ambient Orbs -->
        <div style="position: absolute; top: -80px; left: -80px; width: 250px; height: 250px; background: #10b981; filter: blur(100px); opacity: 0.25; border-radius: 50%; pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; right: -80px; width: 300px; height: 300px; background: #0ea5e9; filter: blur(120px); opacity: 0.2; border-radius: 50%; pointer-events: none;"></div>
        
        <!-- Abstract Grid Overlay -->
        <div style="position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 20px 20px; opacity: 0.2; pointer-events: none;"></div>
        
        <div style="position: relative; z-index: 10; display: flex; flex-direction: column; height: 100%;">
            
            <!-- Top Section: Address -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <p style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Alamat Dompet Blockchain</p>
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span class="hash-display" style="background: rgba(255,255,255,0.08); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.12); color: #cbd5e1; padding: 8px 16px; font-size: 14px; font-family: monospace; border-radius: 8px;">
                            <?= truncateHash($wallet['wallet_address']) ?>
                        </span>
                        <button class="btn-icon" style="color: #a7f3d0; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; width: 36px; height: 36px;" onclick="copyToClipboard('<?= $wallet['wallet_address'] ?>')">
                            <i data-lucide="copy" width="16"></i>
                        </button>
                    </div>
                </div>
                <!-- Optional Web3 Badge right here -->
                <div style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-size: 12px; color: #6ee7b7; border: 1px solid rgba(110, 231, 183, 0.3); display: flex; align-items: center; gap: 6px;">
                    <div style="width: 6px; height: 6px; background: #34d399; border-radius: 50%; box-shadow: 0 0 8px #34d399;"></div> Mainnet Aktif
                </div>
            </div>

            <!-- Middle Section: Massive Balance -->
            <div style="text-align: center; margin: 48px 0;">
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 12px; font-weight: 500;">Total Saldo Aktif</p>
                <div style="display: flex; align-items: baseline; justify-content: center; gap: 12px;">
                    <!-- The value uses CSS Background Clip text to create a metallic/gradient text effect -->
                    <h1 style="font-size: 4.5rem; font-weight: 800; line-height: 1; letter-spacing: -0.04em; margin: 0; background: linear-gradient(to right, #6ee7b7, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        <?= number_format($wallet['saldo_token'], 0, ',', '.') ?> 
                    </h1>
                    <span style="font-size: 1.5rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase;">tCO₂e</span>
                </div>
            </div>

            <!-- Bottom Section: Actions -->
            <div style="display: flex; justify-content: center; gap: 16px; margin-top: auto;">
                <button class="btn-primary" style="background: #10b981; color: white; border: none; padding: 12px 32px; border-radius: 50px; font-weight: 600; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4); display: flex; align-items: center; gap: 8px;" onclick="openModal('modalReceive')">
                    <i data-lucide="arrow-down-to-line" width="18"></i> Terima
                </button>
                <button class="btn-outline" style="background: rgba(255,255,255,0.05); color: white; border: 1px solid rgba(255,255,255,0.2); padding: 12px 32px; border-radius: 50px; font-weight: 600; backdrop-filter: blur(10px); display: flex; align-items: center; gap: 8px;" onclick="openModal('modalSend')">
                    <i data-lucide="send" width="18"></i> Kirim
                </button>
            </div>
            
        </div>
    </div>

    <!-- Tx History -->
    <h3>Riwayat Transaksi (Blockchain)</h3>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Tipe</th>
                    <th>Proyek</th>
                    <th>Jumlah</th>
                    <th>Tx Hash</th>
                    <th>Tanggal</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach($tx_history as $tx): ?>
                <tr>
                    <td>
                        <?php if(strpos($tx['type'], 'Transfer') !== false): ?>
                            <span class="badge badge--transfer"><?= $tx['type'] ?></span>
                        <?php else: ?>
                            <span class="badge badge--rejected"><?= $tx['type'] ?></span>
                        <?php endif; ?>
                    </td>
                    <td><?= $tx['project'] ?></td>
                    <td style="font-weight: 600;"><?= $tx['amount'] ?></td>
                    <td>
                        <span class="hash-display">
                            <?= truncateHash($tx['hash']) ?>
                            <button class="hash-btn" onclick="copyToClipboard('<?= $tx['hash'] ?>')"><i data-lucide="copy" width="12"></i></button>
                        </span>
                    </td>
                    <td class="text-muted text-sm"><?= formatDate($tx['date']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

</div>

<!-- MODALS -->

<!-- Modal Receive -->
<div class="modal-overlay" id="modalReceive">
    <div class="modal-content" style="text-align: center;">
        <button class="modal-close" onclick="closeModal('modalReceive')"><i data-lucide="x" width="20"></i></button>
        <h3 style="margin-bottom: var(--space-sm);">Terima Token</h3>
        <p class="text-sm text-muted" style="margin-bottom: var(--space-lg);">Pindai QR ini atau pantau alamat wallet di bawah untuk menerima transfer dari pihak lain.</p>
        
        <div id="qrcode"></div>
        
        <div style="background: var(--color-bg); padding: var(--space-md); border-radius: var(--radius-md); border: 1px solid var(--color-border); margin-top: var(--space-md);">
            <p class="text-xs text-muted" style="margin-bottom: 8px;">Alamat Wallet Anda (Web3 Mock):</p>
            <div style="display: flex; gap: 8px; align-items: center; justify-content: space-between;">
                <span class="hash-display text-sm" style="flex: 1; text-align: left; overflow: hidden; text-overflow: ellipsis; max-width: 100%; white-space: nowrap;"><?= $wallet['wallet_address'] ?></span>
                <button class="btn-outline btn-sm" onclick="copyToClipboard('<?= $wallet['wallet_address'] ?>')"><i data-lucide="copy" width="14"></i></button>
            </div>
        </div>
    </div>
</div>

<!-- Modal Send -->
<div class="modal-overlay" id="modalSend">
    <div class="modal-content">
        <button class="modal-close" onclick="closeModal('modalSend')"><i data-lucide="x" width="20"></i></button>
        <h3 style="margin-bottom: var(--space-sm);">Kirim Token</h3>
        <p class="text-sm text-muted" style="margin-bottom: var(--space-lg);">Kirim karbon kredit token antar-wallet dengan aman (simulasi).</p>
        
        <form onsubmit="handleSendMock(event)">
            <div class="form-group">
                <label>Alamat Wallet Penerima</label>
                <input type="text" class="form-control" placeholder="0x..." required>
            </div>
            <div class="form-group">
                <label>Jumlah Token (tCO₂e)</label>
                <div style="position: relative;">
                    <input type="number" class="form-control" placeholder="0" min="1" max="<?= $wallet['saldo_token'] ?>" required>
                    <span style="position: absolute; right: 14px; top: 10px; color: var(--color-text-muted); pointer-events: none; font-size: var(--text-sm);">tCO₂e</span>
                </div>
                <p class="text-xs text-muted" style="margin-top: 4px; text-align: right;">Max: <?= number_format($wallet['saldo_token'], 0, ',', '.') ?> tCO₂e</p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-lg); border-top: 1px dashed var(--color-border); padding-top: var(--space-md);">
                <span class="text-sm text-muted">Estimasi Gas Fee</span>
                <span class="text-sm font-mono font-semibold" style="color: var(--color-primary);">~0.002 ETH</span>
            </div>
            <button type="submit" class="btn-primary btn-full">Konfirmasi Pengiriman</button>
        </form>
    </div>
</div>

<!-- Extra Scripts -->
<!-- Include QRCodeLibrary from CDN securely -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script>
// Modal Logic
function openModal(id) {
    document.getElementById(id).classList.add('active');
}
function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}
// Close modal when clicking outside content
document.querySelectorAll('.modal-overlay').forEach(el => {
    el.addEventListener('click', function(e) {
        if(e.target === this) closeModal(this.id);
    });
});

// Generate QR Code dynamically when page loads
window.addEventListener('load', () => {
    const qrContainer = document.getElementById('qrcode');
    qrContainer.innerHTML = ''; // prevent duplicates
    new QRCode(qrContainer, {
        text: "<?= $wallet['wallet_address'] ?>",
        width: 180,
        height: 180,
        colorDark : "#059669",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
    });
});

// Helper for Mock send
function handleSendMock(e) {
    e.preventDefault();
    closeModal('modalSend');
    showToast('Transaksi diproses dengan Smart Contract...', 'info');
    setTimeout(() => {
        showToast('Transfer P2P berhasil dikirim!', 'success');
        e.target.reset(); // clear form
    }, 1500);
}
</script>

<?php require_once '../includes/footer.php'; ?>
