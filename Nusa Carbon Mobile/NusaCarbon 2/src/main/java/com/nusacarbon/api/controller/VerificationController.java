package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.VerificationRequest;
import com.nusacarbon.api.entity.Verification;
import com.nusacarbon.api.service.VerificationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/verifications")
@RequiredArgsConstructor
public class VerificationController {

    private final VerificationService verificationService;

    @PutMapping("/{mrvId}")
    public ResponseEntity<ApiResponse<Map<String, Object>>> submitVerification(
            @PathVariable int mrvId,
            @Valid @RequestBody VerificationRequest request) {
        Verification v = verificationService.submitVerification(mrvId, request);
        Map<String, Object> response = Map.of(
                "id_verifikasi", v.getIdVerifikasi(),
                "id_mrv", v.getMrvReport().getIdMrv(),
                "hasil", v.getHasil().name(),
                "volume_co2e_disetujui", v.getVolumeCo2eDisetujui() != null ? v.getVolumeCo2eDisetujui() : 0,
                "catatan_audit", v.getCatatanAudit() != null ? v.getCatatanAudit() : "",
                "verified_at", v.getVerifiedAt().toString()
        );
        return ResponseEntity.ok(ApiResponse.ok("Verification submitted", response));
    }
}
