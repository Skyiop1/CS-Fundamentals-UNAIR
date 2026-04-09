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

if (!$id_project || $jumlah <= 0) {
    echo json_encode(['success' => false, 'error' => 'Parameter tidak lengkap']);
    exit;
}

try {
    $pdo->beginTransaction();

    // Find active listing
    $stmt = $pdo->prepare("SELECT * FROM listings WHERE id_project = ? AND status_listing = 'active' FOR UPDATE");
    $stmt->execute([$id_project]);
    $listing = $stmt->fetch();

    if (!$listing || $listing['jumlah_token'] < $jumlah) {
        throw new Exception("Stock tidak cukup atau listing tidak valid.");
    }

    // Check buyer IDR balance
    $total_harga = $listing['harga_per_token'] * $jumlah;
    $stmt = $pdo->prepare("SELECT saldo_rupiah FROM wallets WHERE id_user = ? FOR UPDATE");
    $stmt->execute([$_SESSION['user_id']]);
    $buyerWallet = $stmt->fetch();

    if (!$buyerWallet || $buyerWallet['saldo_rupiah'] < $total_harga) {
        throw new Exception("Saldo Rupiah tidak mencukupi untuk transaksi ini.");
    }

    // Insert trade transaction
    $total_harga = $listing['harga_per_token'] * $jumlah;
    $stmt = $pdo->prepare("INSERT INTO trade_transactions (id_listing, buyer_user_id, seller_user_id, total_harga, status) VALUES (?, ?, ?, ?, 'success')");
    $stmt->execute([$listing['id_listing'], $_SESSION['user_id'], $listing['id_user'], $total_harga]);
    $id_transaksi = $pdo->lastInsertId();

    // Update Token Owners (Assume available tokens)
    $stmt = $pdo->prepare("UPDATE carbon_tokens SET status_token = 'sold', owner_user_id = ? WHERE id_project = ? AND status_token IN ('available', 'listed') LIMIT ?");
    $stmt->bindValue(1, $_SESSION['user_id'], PDO::PARAM_INT);
    $stmt->bindValue(2, $id_project, PDO::PARAM_INT);
    $stmt->bindValue(3, $jumlah, PDO::PARAM_INT);
    $stmt->execute();
    
    // Update listing capacity
    $new_stok = $listing['jumlah_token'] - $jumlah;
    $new_status = $new_stok <= 0 ? 'soldout' : 'active';
    $pdo->prepare("UPDATE listings SET jumlah_token = ?, status_listing = ? WHERE id_listing = ?")->execute([$new_stok, $new_status, $listing['id_listing']]);

    // Blockchain LEDGER APPEND
    $txHash = appendToLedger($pdo, 'transfer', $id_transaksi, 'trade_transactions', $jumlah, '0xMarketplaceUser', '0xBuyerVault');

    $pdo->prepare("UPDATE trade_transactions SET tx_transfer_hash = ? WHERE id_transaksi = ?")->execute([$txHash, $id_transaksi]);

    // Give buyer the token balance and deduct IDR
    $pdo->prepare("UPDATE wallets SET saldo_token = saldo_token + ?, saldo_rupiah = saldo_rupiah - ? WHERE id_user = ?")
        ->execute([$jumlah, $total_harga, $_SESSION['user_id']]);

    $pdo->commit();
    echo json_encode(['success' => true, 'tx_hash' => $txHash, 'gas_fee' => mockGasFee()]);

} catch (Exception $e) {
    if ($pdo->inTransaction()) $pdo->rollBack();
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
?>
