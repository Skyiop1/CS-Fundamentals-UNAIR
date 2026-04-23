package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.CertificateResponse;
import com.nusacarbon.api.dto.RetirementRequest;
import com.nusacarbon.api.dto.RetirementResponse;
import com.nusacarbon.api.entity.*;
import com.nusacarbon.api.entity.enums.BlockchainTxType;
import com.nusacarbon.api.entity.enums.RetirementStatus;
import com.nusacarbon.api.entity.enums.TokenStatus;
import com.nusacarbon.api.repository.*;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Year;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class RetirementService {

    private final RetirementRepository retirementRepository;
    private final RetirementDetailRepository retirementDetailRepository;
    private final CarbonTokenRepository tokenRepository;
    private final CertificateRepository certificateRepository;
    private final UserRepository userRepository;
    private final WalletRepository walletRepository;
    private final BlockchainService blockchainService;

    /**
     * Retire tokens — mark as retired (IMMUTABLE), auto-generate certificate,
     * create blockchain retire entries.
     */
    @Transactional
    public RetirementResponse retireTokens(RetirementRequest request) {
        User user = userRepository.findById(request.userId())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        // Validate all tokens belong to user and are available/sold (owned)
        List<CarbonToken> tokens = request.tokenIds().stream()
                .map(id -> tokenRepository.findById(id)
                        .orElseThrow(() -> new EntityNotFoundException("Token not found: " + id)))
                .collect(Collectors.toList());

        for (CarbonToken token : tokens) {
            if (!token.getOwner().getIdUser().equals(request.userId())) {
                throw new IllegalStateException("Token " + token.getIdToken() + " does not belong to user");
            }
            if (token.getStatusToken() == TokenStatus.retired) {
                throw new IllegalStateException("Token " + token.getIdToken() + " is already retired");
            }
            if (token.getStatusToken() == TokenStatus.listed) {
                throw new IllegalStateException("Token " + token.getIdToken() + " is currently listed. Delist before retiring.");
            }
        }

        BigDecimal totalCo2e = BigDecimal.valueOf(tokens.size());

        // Create retirement record
        Retirement retirement = Retirement.builder()
                .user(user)
                .totalCo2e(totalCo2e)
                .alasan(request.alasan())
                .namaEntitas(request.namaEntitas() != null ? request.namaEntitas() : user.getNamaUser())
                .status(RetirementStatus.completed)
                .build();

        Retirement savedRetirement = retirementRepository.save(retirement);

        // Get user wallet address
        String userAddress = walletRepository.findByUserIdUser(user.getIdUser())
                .map(Wallet::getWalletAddress).orElse("0x0000");

        // Retire each token and create retirement details
        for (CarbonToken token : tokens) {
            token.setStatusToken(TokenStatus.retired); // IMMUTABLE after this
            tokenRepository.save(token);

            RetirementDetail detail = RetirementDetail.builder()
                    .retirement(savedRetirement)
                    .token(token)
                    .build();
            retirementDetailRepository.save(detail);
        }

        // Create blockchain retire entry
        blockchainService.createLedgerEntry(
                BlockchainTxType.retire,
                savedRetirement.getIdRetirement(),
                "retirements",
                totalCo2e,
                userAddress,
                "0x0000000000000000000000000000000000000000" // burned to null address
        );

        // Auto-generate certificate
        long certCount = certificateRepository.count();
        String certNumber = String.format("CERT-NC-%d-%03d", Year.now().getValue(), certCount + 1);

        Certificate certificate = Certificate.builder()
                .retirement(savedRetirement)
                .nomorSertifikat(certNumber)
                .namaEntitas(savedRetirement.getNamaEntitas())
                .totalCo2e(totalCo2e)
                .build();

        certificateRepository.save(certificate);

        return toResponse(savedRetirement, certNumber);
    }

    public List<RetirementResponse> getUserRetirements(int userId) {
        return retirementRepository.findByUserIdUserOrderByCreatedAtDesc(userId)
                .stream().map(r -> {
                    String certNum = certificateRepository.findByRetirementIdRetirement(r.getIdRetirement())
                            .map(Certificate::getNomorSertifikat).orElse(null);
                    return toResponse(r, certNum);
                }).collect(Collectors.toList());
    }

    public CertificateResponse getCertificate(int retirementId) {
        Certificate cert = certificateRepository.findByRetirementIdRetirement(retirementId)
                .orElseThrow(() -> new EntityNotFoundException("Certificate not found for retirement: " + retirementId));
        return new CertificateResponse(
                cert.getIdSertifikat(),
                cert.getRetirement().getIdRetirement(),
                cert.getNomorSertifikat(),
                cert.getNamaEntitas(),
                cert.getTotalCo2e(),
                cert.getLinkFilePdf(),
                cert.getNftTokenId(),
                cert.getCreatedAt()
        );
    }

    private RetirementResponse toResponse(Retirement r, String certNumber) {
        return new RetirementResponse(
                r.getIdRetirement(),
                r.getUser().getIdUser(),
                r.getTotalCo2e(),
                r.getAlasan(),
                r.getNamaEntitas(),
                r.getStatus().name(),
                certNumber,
                r.getCreatedAt()
        );
    }
}
