package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record BlockchainTxResponse(
        String txHash,
        String prevHash,
        String txType,
        BigDecimal amountCo2e,
        String fromAddress,
        String toAddress,
        BigDecimal gasFeeMock,
        int blockNumber,
        Integer refId,
        String refTable,
        LocalDateTime createdAt
) {}
