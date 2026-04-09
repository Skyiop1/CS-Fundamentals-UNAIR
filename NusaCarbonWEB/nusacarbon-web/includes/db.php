<?php
// includes/db.php

$host = getenv('MYSQLHOST') ?: 'db';
$db   = getenv('MYSQLDATABASE') ?: 'nusacarbon';
$user = getenv('MYSQLUSER') ?: 'nusa_user';
$pass = getenv('MYSQLPASSWORD') ?: 'nusa_password';
$port = getenv('MYSQLPORT') ?: '3306';
$charset = 'utf8mb4';

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
