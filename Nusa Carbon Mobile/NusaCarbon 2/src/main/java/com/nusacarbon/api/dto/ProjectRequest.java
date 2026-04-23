package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public record ProjectRequest(
        @NotNull Integer idUser,
        @NotNull Integer idKategori,
        @NotBlank String namaProject,
        @NotBlank String lokasi,
        BigDecimal koordinatLat,
        BigDecimal koordinatLng,
        @NotNull BigDecimal luasLahan,
        String deskripsi
) {}
