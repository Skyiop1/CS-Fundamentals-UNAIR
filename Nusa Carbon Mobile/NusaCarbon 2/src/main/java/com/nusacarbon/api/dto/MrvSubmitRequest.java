package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public record MrvSubmitRequest(
        @NotNull Integer idProject,
        @NotNull Integer submittedBy,
        @NotNull String periodeMrv,
        String koordinatGps,
        String linkFotoSatelit,
        BigDecimal estimasiCo2e,
        String catatan
) {}
