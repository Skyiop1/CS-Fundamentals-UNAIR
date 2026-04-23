package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record MrvResponse(
        int idMrv,
        int idProject,
        String namaProject,
        int submittedBy,
        String submitterName,
        String periodeMrv,
        String koordinatGps,
        String linkFotoSatelit,
        BigDecimal estimasiCo2e,
        String catatan,
        String statusMrv,
        LocalDateTime createdAt
) {}
