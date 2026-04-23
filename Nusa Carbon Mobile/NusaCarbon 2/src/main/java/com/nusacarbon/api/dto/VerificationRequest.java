package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public record VerificationRequest(
        @NotNull Integer idVerifier,
        @NotNull String hasil,
        BigDecimal volumeCo2eDisetujui,
        String catatanAudit
) {}
