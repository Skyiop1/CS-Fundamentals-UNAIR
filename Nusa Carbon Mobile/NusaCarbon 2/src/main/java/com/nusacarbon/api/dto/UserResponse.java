package com.nusacarbon.api.dto;

import java.time.LocalDateTime;

public record UserResponse(
        int idUser,
        String namaUser,
        String email,
        String noHp,
        String statusKyc,
        String roleName,
        LocalDateTime createdAt
) {}
