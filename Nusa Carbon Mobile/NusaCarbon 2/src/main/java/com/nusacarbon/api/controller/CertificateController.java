package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.CertificateResponse;
import com.nusacarbon.api.service.RetirementService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/certificates")
@RequiredArgsConstructor
public class CertificateController {

    private final RetirementService retirementService;

    @GetMapping("/{retirementId}")
    public ResponseEntity<ApiResponse<CertificateResponse>> getCertificate(
            @PathVariable int retirementId) {
        CertificateResponse certificate = retirementService.getCertificate(retirementId);
        return ResponseEntity.ok(ApiResponse.ok(certificate));
    }
}
