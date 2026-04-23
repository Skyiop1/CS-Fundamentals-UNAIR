package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.WalletResponse;
import com.nusacarbon.api.entity.Wallet;
import com.nusacarbon.api.entity.enums.TokenStatus;
import com.nusacarbon.api.repository.CarbonTokenRepository;
import com.nusacarbon.api.repository.WalletRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class WalletService {

    private final WalletRepository walletRepository;
    private final CarbonTokenRepository tokenRepository;

    public WalletResponse getWalletByUserId(int userId) {
        Wallet wallet = walletRepository.findByUserIdUser(userId)
                .orElseThrow(() -> new EntityNotFoundException("Wallet not found for user: " + userId));

        long totalTokens = tokenRepository.countByOwnerIdUser(userId);
        long available = tokenRepository.countByOwnerIdUserAndStatusToken(userId, TokenStatus.available);
        long listed = tokenRepository.countByOwnerIdUserAndStatusToken(userId, TokenStatus.listed);
        long sold = tokenRepository.countByOwnerIdUserAndStatusToken(userId, TokenStatus.sold);
        long retired = tokenRepository.countByOwnerIdUserAndStatusToken(userId, TokenStatus.retired);

        return new WalletResponse(
                wallet.getIdWallet(),
                wallet.getUser().getIdUser(),
                wallet.getWalletAddress(),
                wallet.getChainNetwork(),
                totalTokens,
                available,
                listed,
                sold,
                retired,
                wallet.getCreatedAt()
        );
    }
}
