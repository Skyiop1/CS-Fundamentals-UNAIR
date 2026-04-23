package com.nusacarbon.api.dto;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.util.List;

public record RetirementRequest(
        @NotNull Integer userId,
        @NotEmpty List<Integer> tokenIds,
        String alasan,
        String namaEntitas
) {}
