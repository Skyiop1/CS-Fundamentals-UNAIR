package com.nusacarbon.api.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record CertificateResponse(
        int idSertifikat,
        int idRetirement,
        String nomorSertifikat,
        String namaEntitas,
        BigDecimal totalCo2e,
        String linkFilePdf,
        String nftTokenId,
        LocalDateTime createdAt
) {}
