<?php
// includes/db.php

$host = 'db';
$db = 'nusacarbon';
$user = 'nusa_user';
$pass = 'nusa_password';
$port = '3306';
$charset = 'utf8mb4';

// HARDCODE URL PUBLIK RAILWAY (Anti Gagal)
// Jika di server live, paksa pakai ini!
$railwayPublicUrl = 'mysql://root:BGfDBOxTobfmWYFgdotV]liwPAZEYM@mainline.proxy.rlwy.net:22385/railway';

$dbUrl = getenv('MYSQL_URL') ?: getenv('MYSQL_PUBLIC_URL') ?: getenv('DATABASE_URL');
if (!$dbUrl) {
    // Jika tidak terbaca variabel environment, paksa gunakan hardcode!
    $dbUrl = $railwayPublicUrl;
} else if (strpos($dbUrl, 'railway.internal') !== false) {
    // Jika Railway mencoba memaksa jalur internal yang error, timpuk pakai jalur publik!
    $dbUrl = $railwayPublicUrl;
}

// 2. Parsing URL agar PHP tidak akan mungkin meleset membaca password
if ($dbUrl) {
    $parsed = parse_url($dbUrl);
    if ($parsed) {
        $host = $parsed['host'] ?? $host;
        $port = $parsed['port'] ?? $port;
        $user = $parsed['user'] ?? $user;
        $pass = $parsed['pass'] ?? $pass;
        $db = ltrim($parsed['path'], '/') ?: $db;
    }
} else {
    // 3. Cadangan jika tidak pakai URL, ambil dari individual variable
    $host = getenv('MYSQLHOST') ?: (isset($_SERVER['MYSQLHOST']) ? $_SERVER['MYSQLHOST'] : $host);
    $db = getenv('MYSQLDATABASE') ?: (isset($_SERVER['MYSQLDATABASE']) ? $_SERVER['MYSQLDATABASE'] : $db);
    $user = getenv('MYSQLUSER') ?: (isset($_SERVER['MYSQLUSER']) ? $_SERVER['MYSQLUSER'] : $user);
    $pass = getenv('MYSQLPASSWORD') ?: (isset($_SERVER['MYSQLPASSWORD']) ? $_SERVER['MYSQLPASSWORD'] : $pass);
    $port = getenv('MYSQLPORT') ?: (isset($_SERVER['MYSQLPORT']) ? $_SERVER['MYSQLPORT'] : $port);
}

$dsn = "mysql:host=$host;port=$port;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
    
    // Auto-migrate schema for user feature request (IDR Balance & Token Tracking)
    try {
        $pdo->exec("ALTER TABLE wallets ADD COLUMN saldo_rupiah DECIMAL(16,2) DEFAULT 1000000000.00");
        $pdo->exec("UPDATE wallets SET saldo_rupiah = 1000000000.00 WHERE saldo_rupiah IS NULL");
        $pdo->exec("ALTER TABLE trade_transactions ADD COLUMN jumlah_token INT AFTER total_harga");
    } catch(Exception $e) {} // Ignore if already exists

} catch (\PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}
?>