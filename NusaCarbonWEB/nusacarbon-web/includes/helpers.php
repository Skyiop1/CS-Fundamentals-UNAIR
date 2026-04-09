<?php
// includes/helpers.php

function formatIDR(float $amount): string {
    return 'Rp ' . number_format($amount, 0, ',', '.');
}

function formatCO2e(float $amount, int $decimals = 0): string {
    return number_format($amount, $decimals, ',', '.') . ' tCO₂e';
}

function truncateHash(string $hash, int $prefixLen = 6, int $suffixLen = 4): string {
    if (strlen($hash) <= $prefixLen + $suffixLen + 3) return $hash;
    return substr($hash, 0, $prefixLen) . '...' . substr($hash, -$suffixLen);
}

function formatDate(string $datetime): string {
    $months = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];
    $d = new DateTime($datetime);
    return $d->format('d') . ' ' . $months[(int)$d->format('m') - 1] . ' ' . $d->format('Y');
}

function generateMockWalletAddress(): string {
    return '0x' . bin2hex(random_bytes(20));
}

function generateTokenSerial(int $year, int $projectId, int $seq): string {
    return sprintf('NC-%d-%03d-%06d', $year, $projectId, $seq);
}

function generateCertNumber(int $year, int $seq): string {
    return sprintf('CERT-NC-%d-%03d', $year, $seq);
}
?>
