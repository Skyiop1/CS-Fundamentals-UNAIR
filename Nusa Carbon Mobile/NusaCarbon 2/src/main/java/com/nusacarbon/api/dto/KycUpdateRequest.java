package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotNull;

public record KycUpdateRequest(
        @NotNull String statusKyc
) {}
