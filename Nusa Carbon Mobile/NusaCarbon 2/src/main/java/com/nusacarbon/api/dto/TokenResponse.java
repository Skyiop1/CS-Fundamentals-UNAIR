package com.nusacarbon.api.dto;

import java.time.LocalDateTime;

public record TokenResponse(
        int idToken,
        String tokenSerial,
        int vintageYear,
        String statusToken,
        String txMintHash,
        String metadataHash,
        int idProject,
        String namaProject,
        String lokasi,
        String namaKategori,
        String imageUrl,
        int ownerUserId,
        String ownerName,
        LocalDateTime createdAt
) {}
