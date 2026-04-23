package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public record ListingRequest(
        @NotNull Integer idUser,
        @NotNull Integer idProject,
        @NotNull BigDecimal hargaPerToken,
        @NotNull Integer jumlahToken
) {}
