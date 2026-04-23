package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record TradeRequest(
        @NotNull Integer idListing,
        @NotNull Integer buyerUserId,
        @NotNull Integer jumlah,
        @NotBlank String metodeBayar
) {}
