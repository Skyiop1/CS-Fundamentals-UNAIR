<?php
require_once 'includes/db.php';
try {
    $pdo->exec("ALTER TABLE wallets ADD COLUMN saldo_rupiah DECIMAL(16,2) DEFAULT 1000000000"); // 1 Billion IDR mock
    $pdo->exec("UPDATE wallets SET saldo_rupiah = 1000000000"); // Backfill existing
    echo "Success";
} catch(Exception $e) {
    if(strpos($e->getMessage(), 'Duplicate column name') !== false) {
        echo "Already exists";
    } else {
        echo "Error: " . $e->getMessage();
    }
}
?>
