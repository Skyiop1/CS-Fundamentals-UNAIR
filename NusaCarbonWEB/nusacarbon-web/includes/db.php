<?php
// includes/db.php

$host = 'db'; // Docker service name
$db   = 'nusacarbon';
$user = 'nusa_user';
$pass = 'nusa_password';
$port = '3306';
$charset = 'utf8mb4';

// 1. Cek Variabel Lengkap dari Railway untuk menghindari typo manual
$dbUrl = getenv('MYSQL_URL') ?: getenv('MYSQL_PUBLIC_URL') ?: getenv('DATABASE_URL');
if (!$dbUrl) {
    if (isset($_SERVER['MYSQL_URL'])) $dbUrl = $_SERVER['MYSQL_URL'];
    elseif (isset($_SERVER['MYSQL_PUBLIC_URL'])) $dbUrl = $_SERVER['MYSQL_PUBLIC_URL'];
}

// 2. Parsing URL agar PHP tidak akan mungkin meleset membaca password
if ($dbUrl) {
    $parsed = parse_url($dbUrl);
    if ($parsed) {
        $host = $parsed['host'] ?? $host;
        $port = $parsed['port'] ?? $port;
        $user = $parsed['user'] ?? $user;
        $pass = $parsed['pass'] ?? $pass;
        $db   = ltrim($parsed['path'], '/') ?: $db;
    }
} else {
    // 3. Cadangan jika tidak pakai URL, ambil dari individual variable
    $host = getenv('MYSQLHOST') ?: (isset($_SERVER['MYSQLHOST']) ? $_SERVER['MYSQLHOST'] : $host);
    $db   = getenv('MYSQLDATABASE') ?: (isset($_SERVER['MYSQLDATABASE']) ? $_SERVER['MYSQLDATABASE'] : $db);
    $user = getenv('MYSQLUSER') ?: (isset($_SERVER['MYSQLUSER']) ? $_SERVER['MYSQLUSER'] : $user);
    $pass = getenv('MYSQLPASSWORD') ?: (isset($_SERVER['MYSQLPASSWORD']) ? $_SERVER['MYSQLPASSWORD'] : $pass);
    $port = getenv('MYSQLPORT') ?: (isset($_SERVER['MYSQLPORT']) ? $_SERVER['MYSQLPORT'] : $port);
}

$dsn = "mysql:host=$host;port=$port;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}
?>
