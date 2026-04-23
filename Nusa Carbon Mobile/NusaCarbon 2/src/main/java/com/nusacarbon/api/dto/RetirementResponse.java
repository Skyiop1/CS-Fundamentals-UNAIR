package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record RetirementResponse(
        int idRetirement,
        int idUser,
        BigDecimal totalCo2e,
        String alasan,
        String namaEntitas,
        String status,
        String nomorSertifikat,
        LocalDateTime createdAt
) {}
