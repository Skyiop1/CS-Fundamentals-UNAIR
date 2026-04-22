<?php
// api/buy-token.php
require_once '../includes/auth.php';
requireRole('buyer');
require_once '../includes/db.php';
require_once '../includes/blockchain.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'error' => 'Invalid method']);
    exit;
}

$id_project = $_POST['id_project'] ?? null;
$jumlah = (int)($_POST['jumlah_token'] ?? 0);
$buyer_user_id = (int)$_SESSION['user_id'];

if (!$id_project || $jumlah <= 0) {
    echo json_encode(['success' => false, 'error' => 'Parameter tidak lengkap']);
    exit;
}

try {
    $pdo->beginTransaction();

    // ─── Step 1: Validasi listing (active & stock cukup) ───
    $stmt = $pdo->prepare("SELECT * FROM listings WHERE id_project = ? AND status_listing = 'active' FOR UPDATE");
    $stmt->execute([$id_project]);
    $listing = $stmt->fetch();

    if (!$listing || $listing['jumlah_token'] < $jumlah) {
        throw new Exception("Stock tidak cukup atau listing tidak valid.");
    }

    // ─── Step 2: Validasi saldo rupiah buyer ───
    $total_harga = $listing['harga_per_token'] * $jumlah;
    $stmt = $pdo->prepare("SELECT saldo_rupiah FROM wallets WHERE id_user = ? FOR UPDATE");
    $stmt->execute([$buyer_user_id]);
    $buyerWallet = $stmt->fetch();

    if (!$buyerWallet || $buyerWallet['saldo_rupiah'] < $total_harga) {
        throw new Exception("Saldo Rupiah tidak mencukupi untuk transaksi ini.");
    }

    // ─── Step 3: INSERT trade_transactions (status = 'pending') ───
    $stmt = $pdo->prepare(
        "INSERT INTO trade_transactions (id_listing, buyer_user_id, seller_user_id, total_harga, jumlah_token, status)
         VALUES (?, ?, ?, ?, ?, 'pending')"
    );
    $stmt->execute([$listing['id_listing'], $buyer_user_id, $listing['id_user'], $total_harga, $jumlah]);
    $id_transaksi = $pdo->lastInsertId();

    // ─── Step 4: Ambil id_token dari carbon_tokens yang available ───
    $stmt = $pdo->prepare(
        "SELECT id_token FROM carbon_tokens
         WHERE id_project = ? AND status_token IN ('available', 'listed')
         ORDER BY id_token ASC
         LIMIT ?"
    );
    $stmt->bindValue(1, (int)$id_project, PDO::PARAM_INT);
    $stmt->bindValue(2, $jumlah, PDO::PARAM_INT);
    $stmt->execute();
    $tokenRows = $stmt->fetchAll(PDO::FETCH_COLUMN);

    if (count($tokenRows) < $jumlah) {
        throw new Exception("Token fisik tidak cukup tersedia di database (butuh {$jumlah}, tersedia " . count($tokenRows) . ").");
    }

    // ─── Step 5: INSERT trade_details per token ───
    $stmtDetail = $pdo->prepare(
        "INSERT INTO trade_details (id_transaksi, id_token, harga_token) VALUES (?, ?, ?)"
    );
    foreach ($tokenRows as $tokenId) {
        $stmtDetail->execute([$id_transaksi, $tokenId, $listing['harga_per_token']]);
    }

    // ─── Step 6: UPDATE carbon_tokens ownership → buyer ───
    $placeholders = implode(',', array_fill(0, count($tokenRows), '?'));
    $stmt = $pdo->prepare(
        "UPDATE carbon_tokens SET status_token = 'sold', owner_user_id = ?
         WHERE id_token IN ({$placeholders})"
    );
    $stmt->execute(array_merge([$buyer_user_id], $tokenRows));

    // ─── Step 7: UPDATE wallet buyer (saldo_token +, saldo_rupiah -) ───
    $stmt = $pdo->prepare(
        "UPDATE wallets SET saldo_token = saldo_token + ?, saldo_rupiah = saldo_rupiah - ?
         WHERE id_user = ?"
    );
    $stmt->execute([$jumlah, $total_harga, $buyer_user_id]);

    // ─── Step 8: UPDATE listing stock ───
    $new_stok = $listing['jumlah_token'] - $jumlah;
    $new_status = $new_stok <= 0 ? 'soldout' : 'active';
    $pdo->prepare("UPDATE listings SET jumlah_token = ?, status_listing = ? WHERE id_listing = ?")
        ->execute([$new_stok, $new_status, $listing['id_listing']]);

    // ─── Step 9: Append ke blockchain ledger ───
    $txHash = appendToLedger(
        $pdo, 'transfer', $id_transaksi, 'trade_transactions',
        $jumlah, '0xMarketplaceUser', '0xBuyerVault'
    );

    // ─── Step 10: UPDATE trade_transactions → success + tx_hash ───
    $pdo->prepare("UPDATE trade_transactions SET status = 'success', tx_transfer_hash = ? WHERE id_transaksi = ?")
        ->execute([$txHash, $id_transaksi]);

    $pdo->commit();
    echo json_encode(['success' => true, 'tx_hash' => $txHash, 'gas_fee' => mockGasFee()]);

} catch (Exception $e) {
    if ($pdo->inTransaction()) $pdo->rollBack();
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
?>
