package com.nusacarbon.api.dto;

import java.time.LocalDateTime;

public record WalletResponse(
        int idWallet,
        int idUser,
        String walletAddress,
        String chainNetwork,
        long totalTokens,
        long availableTokens,
        long listedTokens,
        long soldTokens,
        long retiredTokens,
        LocalDateTime createdAt
) {}
