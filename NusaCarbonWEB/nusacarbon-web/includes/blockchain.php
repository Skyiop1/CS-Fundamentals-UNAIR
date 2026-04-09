<?php
// includes/blockchain.php

define('GENESIS_HASH', '0x' . str_repeat('0', 64));

function generateTxHash(string $prevHash, string $type, float $amount, int $refId, string $timestamp): string {
    $input = "{$prevHash}|{$type}|{$amount}|{$refId}|{$timestamp}";
    return '0x' . hash('sha256', $input);
}

function truncateHashStr(string $hash): string {
    if (strlen($hash) < 12) return $hash;
    return substr($hash, 0, 6) . '...' . substr($hash, -4);
}

function mockGasFee(): float {
    $fees = [0.003, 0.004, 0.005, 0.006, 0.007];
    return $fees[(int)(microtime(true) * 1000) % count($fees)];
}

function getLatestBlockHash(PDO $pdo): string {
    $stmt = $pdo->query("SELECT tx_hash FROM blockchain_ledger ORDER BY id DESC LIMIT 1");
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    return $row ? $row['tx_hash'] : GENESIS_HASH;
}

function getLatestBlockNumber(PDO $pdo): int {
    return (int)$pdo->query("SELECT COUNT(*) FROM blockchain_ledger")->fetchColumn();
}

function appendToLedger(PDO $pdo, string $type, int $refId, string $refTable, float $amount, ?string $fromAddr, ?string $toAddr): string {
    $prevHash    = getLatestBlockHash($pdo);
    $timestamp   = date('Y-m-d H:i:s');
    $txHash      = generateTxHash($prevHash, $type, $amount, $refId, $timestamp);
    $blockNumber = getLatestBlockNumber($pdo) + 1;
    $gasFee      = mockGasFee();

    $stmt = $pdo->prepare(
        "INSERT INTO blockchain_ledger 
         (block_number, tx_hash, prev_hash, tx_type, ref_id, ref_table, amount_co2e, from_address, to_address, gas_fee_mock)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    );
    $stmt->execute([$blockNumber, $txHash, $prevHash, $type, $refId, $refTable, $amount, $fromAddr, $toAddr, $gasFee]);

    return $txHash;
}
?>
