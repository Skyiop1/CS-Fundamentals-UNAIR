package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.MintRequest;
import com.nusacarbon.api.dto.TokenResponse;
import com.nusacarbon.api.entity.CarbonToken;
import com.nusacarbon.api.entity.Verification;
import com.nusacarbon.api.entity.enums.BlockchainTxType;
import com.nusacarbon.api.entity.enums.TokenStatus;
import com.nusacarbon.api.entity.enums.VerificationResult;
import com.nusacarbon.api.repository.CarbonTokenRepository;
import com.nusacarbon.api.repository.VerificationRepository;
import com.nusacarbon.api.repository.WalletRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class TokenService {

    private final CarbonTokenRepository tokenRepository;
    private final VerificationRepository verificationRepository;
    private final WalletRepository walletRepository;
    private final BlockchainService blockchainService;

    public List<TokenResponse> getTokens(Integer userId, String status, Integer vintage) {
        List<CarbonToken> tokens;
        if (userId != null && status != null && vintage != null) {
            tokens = tokenRepository.findByOwnerIdUserAndStatusTokenAndVintageYear(
                    userId, TokenStatus.valueOf(status), vintage);
        } else if (userId != null && status != null) {
            tokens = tokenRepository.findByOwnerIdUserAndStatusToken(userId, TokenStatus.valueOf(status));
        } else if (userId != null) {
            tokens = tokenRepository.findByOwnerIdUser(userId);
        } else if (status != null) {
            tokens = tokenRepository.findByStatusToken(TokenStatus.valueOf(status));
        } else {
            tokens = tokenRepository.findAll();
        }
        return tokens.stream().map(this::toResponse).collect(Collectors.toList());
    }

    public TokenResponse getTokenById(int id) {
        CarbonToken token = tokenRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Token not found"));
        return toResponse(token);
    }

    /**
     * Mint tokens — only if verification is approved.
     * Serial format: NC-{YEAR}-{PROJECT_ID_3DIGIT}-{SEQ_6DIGIT}
     */
    @Transactional
    public List<TokenResponse> mintTokens(MintRequest request) {
        Verification verification = verificationRepository.findById(request.idVerifikasi())
                .orElseThrow(() -> new EntityNotFoundException("Verification not found"));

        if (verification.getHasil() != VerificationResult.approved) {
            throw new IllegalStateException("Tokens can only be minted after verification is approved");
        }

        var project = verification.getMrvReport().getProject();
        var owner = project.getUser();

        // Get current token count for this project to generate sequential serials
        long existingCount = tokenRepository.findByProjectIdProject(project.getIdProject()).size();

        // Get wallet address for blockchain entry
        String ownerAddress = walletRepository.findByUserIdUser(owner.getIdUser())
                .map(w -> w.getWalletAddress())
                .orElse("0x0000000000000000000000000000000000000000");

        List<CarbonToken> minted = new ArrayList<>();

        for (int i = 0; i < request.quantity(); i++) {
            long seq = existingCount + i + 1;
            String serial = String.format("NC-%d-%03d-%06d",
                    request.vintageYear(), project.getIdProject(), seq);

            CarbonToken token = CarbonToken.builder()
                    .project(project)
                    .verification(verification)
                    .owner(owner)
                    .tokenSerial(serial)
                    .vintageYear(request.vintageYear())
                    .statusToken(TokenStatus.available)
                    .build();

            CarbonToken saved = tokenRepository.save(token);

            // Create blockchain ledger entry for mint
            var ledgerEntry = blockchainService.createLedgerEntry(
                    BlockchainTxType.mint,
                    saved.getIdToken(),
                    "carbon_tokens",
                    BigDecimal.ONE, // 1 tCO2e per token
                    "0x0000000000000000000000000000000000000000", // from genesis
                    ownerAddress
            );

            saved.setTxMintHash(ledgerEntry.getTxHash());
            tokenRepository.save(saved);
            minted.add(saved);
        }

        return minted.stream().map(this::toResponse).collect(Collectors.toList());
    }

    public TokenResponse toResponse(CarbonToken t) {
        return new TokenResponse(
                t.getIdToken(),
                t.getTokenSerial(),
                t.getVintageYear(),
                t.getStatusToken().name(),
                t.getTxMintHash(),
                t.getMetadataHash(),
                t.getProject().getIdProject(),
                t.getProject().getNamaProject(),
                t.getProject().getLokasi(),
                t.getProject().getKategori().getNamaKategori(),
                t.getProject().getImageUrl(),
                t.getOwner().getIdUser(),
                t.getOwner().getNamaUser(),
                t.getCreatedAt()
        );
    }
}
