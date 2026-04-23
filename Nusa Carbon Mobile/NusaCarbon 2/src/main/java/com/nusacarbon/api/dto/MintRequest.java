package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotNull;

public record MintRequest(
        @NotNull Integer idVerifikasi,
        @NotNull Integer quantity,
        @NotNull Integer vintageYear
) {}
