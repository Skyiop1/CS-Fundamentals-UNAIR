<?php
// includes/auth.php
session_start();

function requireRole(string ...$allowedRoles): void {
    if (!isset($_SESSION['user_id']) || !isset($_SESSION['role']) || !in_array($_SESSION['role'], $allowedRoles)) {
        header('Location: /login.php?redirect=' . urlencode($_SERVER['REQUEST_URI']));
        exit;
    }
}
?>
