<?php
// api/retire-token.php
require_once '../includes/auth.php';
requireRole('buyer', 'owner');
require_once '../includes/db.php';
require_once '../includes/blockchain.php';
require_once '../includes/helpers.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'error' => 'Invalid method']);
    exit;
}

$jumlah = (int)($_POST['jumlah_co2e'] ?? 0);
$entitas = $_POST['nama_entitas'] ?? 'Anonymous Entity';

if ($jumlah <= 0) {
    echo json_encode(['success' => false, 'error' => 'Jumlah tidak valid']);
    exit;
}

try {
    $pdo->beginTransaction();

    // Insert retirements record
    $stmt = $pdo->prepare("INSERT INTO retirements (id_user, nama_entitas, total_co2e) VALUES (?, ?, ?)");
    $stmt->execute([$_SESSION['user_id'], $entitas, $jumlah]);
    $id_retire = $pdo->lastInsertId();

    // Burn tokens logic (update status to retired)
    $stmt = $pdo->prepare("UPDATE carbon_tokens SET status_token = 'retired' WHERE owner_user_id = ? AND status_token IN ('sold', 'available') LIMIT ?");
    $stmt->bindValue(1, $_SESSION['user_id'], PDO::PARAM_INT);
    $stmt->bindValue(2, $jumlah, PDO::PARAM_INT);
    $stmt->execute();

    // Append to Blockchain
    $txHash = appendToLedger($pdo, 'retire', $id_retire, 'retirements', $jumlah, '0xUserVault', '0xNullAddress');
    $pdo->prepare("UPDATE retirements SET tx_retirement_hash = ? WHERE id_retirement = ?")->execute([$txHash, $id_retire]);

    // Issue Certificate
    $certNo = generateCertNumber(date('Y'), $id_retire);
    $pdo->prepare("INSERT INTO certificates (id_retirement, nomor_sertifikat, nama_entitas, total_co2e) VALUES (?, ?, ?, ?)")->execute([$id_retire, $certNo, $entitas, $jumlah]);

    // Subtract from Wallet
    $pdo->prepare("UPDATE wallets SET saldo_token = saldo_token - ? WHERE id_user = ?")->execute([$jumlah, $_SESSION['user_id']]);

    $pdo->commit();
    echo json_encode(['success' => true, 'tx_hash' => $txHash, 'certificate_id' => $certNo]);

} catch (Exception $e) {
    if ($pdo->inTransaction()) $pdo->rollBack();
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
?>
