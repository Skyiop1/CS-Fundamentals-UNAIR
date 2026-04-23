package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record TradeResponse(
        int idTransaksi,
        int idListing,
        int buyerUserId,
        String buyerName,
        int sellerUserId,
        String sellerName,
        BigDecimal totalHarga,
        String metodeBayar,
        String status,
        String txTransferHash,
        String namaProject,
        int tokenCount,
        LocalDateTime tanggalTransaksi
) {}
