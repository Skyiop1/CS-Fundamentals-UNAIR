package com.nusacarbon.api.util;

import com.nusacarbon.api.repository.BlockchainLedgerRepository;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class BlockchainHashUtil {

    public static final String GENESIS_HASH =
            "0x0000000000000000000000000000000000000000000000000000000000000000";

    /**
     * Generate SHA-256 hash linking to previous block.
     */
    public static String generateTxHash(
            String previousHash,
            String txType,
            double amount,
            int refId,
            String timestamp
    ) {
        String input = previousHash + "|" + txType + "|" + amount + "|" + refId + "|" + timestamp;
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(input.getBytes(StandardCharsets.UTF_8));
            StringBuilder hex = new StringBuilder("0x");
            for (byte b : hashBytes) {
                hex.append(String.format("%02x", b));
            }
            return hex.toString();
        } catch (Exception e) {
            throw new RuntimeException("Hash generation failed", e);
        }
    }

    /**
     * Get the last block's hash (or GENESIS_HASH if empty).
     */
    public static String getPreviousHash(BlockchainLedgerRepository repo) {
        return repo.findTopByOrderByBlockNumberDesc()
                .map(ledger -> ledger.getTxHash())
                .orElse(GENESIS_HASH);
    }

    /**
     * Get the last block number (or 0 if empty).
     */
    public static int getLastBlockNumber(BlockchainLedgerRepository repo) {
        return repo.findTopByOrderByBlockNumberDesc()
                .map(ledger -> ledger.getBlockNumber())
                .orElse(0);
    }

    /**
     * Generate mock gas fee between 0.003–0.007.
     */
    public static double mockGasFee() {
        double[] fees = {0.003, 0.004, 0.005, 0.006, 0.007};
        return fees[(int) (System.currentTimeMillis() % fees.length)];
    }
}
