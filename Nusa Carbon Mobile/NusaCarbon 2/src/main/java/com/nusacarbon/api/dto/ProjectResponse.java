package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record ProjectResponse(
        int idProject,
        String namaProject,
        String lokasi,
        String namaKategori,
        String statusProject,
        BigDecimal luasLahan,
        BigDecimal koordinatLat,
        BigDecimal koordinatLng,
        String deskripsi,
        String imageUrl,
        int idUser,
        String ownerName,
        LocalDateTime createdAt,
        LocalDateTime updatedAt
) {}
