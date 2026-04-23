package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record ListingResponse(
        int idListing,
        String namaProject,
        String lokasi,
        String namaKategori,
        BigDecimal hargaPerToken,
        int jumlahToken,
        String statusListing,
        int sellerUserId,
        String sellerName,
        int idProject,
        LocalDateTime createdAt
) {}
