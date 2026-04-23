package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.VerificationRequest;
import com.nusacarbon.api.entity.MrvReport;
import com.nusacarbon.api.entity.User;
import com.nusacarbon.api.entity.Verification;
import com.nusacarbon.api.entity.enums.MrvStatus;
import com.nusacarbon.api.entity.enums.VerificationResult;
import com.nusacarbon.api.repository.UserRepository;
import com.nusacarbon.api.repository.VerificationRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class VerificationService {

    private final VerificationRepository verificationRepository;
    private final UserRepository userRepository;
    private final MrvService mrvService;

    @Transactional
    public Verification submitVerification(int mrvId, VerificationRequest request) {
        MrvReport mrvReport = mrvService.getMrvEntity(mrvId);

        User verifier = userRepository.findById(request.idVerifier())
                .orElseThrow(() -> new EntityNotFoundException("Verifier not found"));

        VerificationResult hasil = VerificationResult.valueOf(request.hasil());

        Verification verification = Verification.builder()
                .mrvReport(mrvReport)
                .verifier(verifier)
                .hasil(hasil)
                .volumeCo2eDisetujui(request.volumeCo2eDisetujui())
                .catatanAudit(request.catatanAudit())
                .build();

        Verification saved = verificationRepository.save(verification);

        // Update MRV status based on verification result
        switch (hasil) {
            case approved -> mrvService.updateMrvStatus(mrvId, MrvStatus.reviewed);
            case rejected -> mrvService.updateMrvStatus(mrvId, MrvStatus.reviewed);
            case revision_needed -> mrvService.updateMrvStatus(mrvId, MrvStatus.revision_needed);
        }

        return saved;
    }
}
