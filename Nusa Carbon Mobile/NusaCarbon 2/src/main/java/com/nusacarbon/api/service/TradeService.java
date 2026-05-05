package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.*;
import com.nusacarbon.api.entity.*;
import com.nusacarbon.api.entity.enums.*;
import com.nusacarbon.api.repository.*;
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
public class TradeService {

    private final TradeTransactionRepository transactionRepository;
    private final TradeDetailRepository tradeDetailRepository;
    private final ListingRepository listingRepository;
    private final CarbonTokenRepository tokenRepository;
    private final UserRepository userRepository;
    private final WalletRepository walletRepository;
    private final BlockchainService blockchainService;

    public List<ListingResponse> getActiveListings(String kategori) {
        List<Listing> listings;
        if (kategori != null && !kategori.isBlank()) {
            listings = listingRepository
                    .findByStatusListingAndProjectKategoriNamaKategoriIgnoreCase(
                            ListingStatus.active, kategori);
        } else {
            listings = listingRepository.findByStatusListing(ListingStatus.active);
        }
        return listings.stream().map(this::toListingResponse).collect(Collectors.toList());
    }

    @Transactional
    public ListingResponse createListing(ListingRequest request) {
        User seller = userRepository.findById(request.idUser())
                .orElseThrow(() -> new EntityNotFoundException("Seller not found"));
        Project project = tokenRepository.findByOwnerIdUserAndStatusToken(request.idUser(), TokenStatus.available)
                .stream()
                .filter(t -> t.getProject().getIdProject().equals(request.idProject()))
                .findFirst()
                .map(CarbonToken::getProject)
                .orElseThrow(() -> new IllegalStateException("No available tokens found for this project"));

        // Verify seller has enough available tokens
        long availableCount = tokenRepository.findByOwnerIdUserAndStatusToken(request.idUser(), TokenStatus.available)
                .stream()
                .filter(t -> t.getProject().getIdProject().equals(request.idProject()))
                .count();

        if (availableCount < request.jumlahToken()) {
            throw new IllegalStateException("Not enough available tokens. You have " + availableCount);
        }

        // Mark tokens as listed
        List<CarbonToken> tokensToList = tokenRepository.findByOwnerIdUserAndStatusToken(request.idUser(), TokenStatus.available)
                .stream()
                .filter(t -> t.getProject().getIdProject().equals(request.idProject()))
                .limit(request.jumlahToken())
                .collect(Collectors.toList());

        tokensToList.forEach(t -> {
            t.setStatusToken(TokenStatus.listed);
            tokenRepository.save(t);
        });

        Listing listing = Listing.builder()
                .seller(seller)
                .project(project)
                .hargaPerToken(request.hargaPerToken())
                .jumlahToken(request.jumlahToken())
                .statusListing(ListingStatus.active)
                .build();

        Listing saved = listingRepository.save(listing);
        return toListingResponse(saved);
    }

    /**
     * Execute trade: create transaction, update token ownership, blockchain transfer entry.
     */
    @Transactional
    public TradeResponse executeTrade(TradeRequest request) {
        Listing listing = listingRepository.findById(request.idListing())
                .orElseThrow(() -> new EntityNotFoundException("Listing not found"));

        if (listing.getStatusListing() != ListingStatus.active) {
            throw new IllegalStateException("Listing is not active");
        }

        if (request.jumlah() > listing.getJumlahToken()) {
            throw new IllegalStateException("Requested quantity exceeds available tokens");
        }

        User buyer = userRepository.findById(request.buyerUserId())
                .orElseThrow(() -> new EntityNotFoundException("Buyer not found"));
        User seller = listing.getSeller();

        BigDecimal totalPrice = listing.getHargaPerToken().multiply(BigDecimal.valueOf(request.jumlah()));

        // Create transaction
        TradeTransaction transaction = TradeTransaction.builder()
                .listing(listing)
                .buyer(buyer)
                .seller(seller)
                .totalHarga(totalPrice)
                .metodeBayar(request.metodeBayar())
                .status(TxStatus.success) // Mock: instant success
                .build();

        TradeTransaction savedTx = transactionRepository.save(transaction);

        // Get listed tokens from seller for this project
        List<CarbonToken> listedTokens = tokenRepository.findByOwnerIdUserAndStatusToken(
                        seller.getIdUser(), TokenStatus.listed)
                .stream()
                .filter(t -> t.getProject().getIdProject().equals(listing.getProject().getIdProject()))
                .limit(request.jumlah())
                .collect(Collectors.toList());

        // Get wallets
        Wallet sellerWallet = walletRepository.findByUserIdUser(seller.getIdUser())
                .orElseThrow(() -> new EntityNotFoundException("Seller wallet not found"));
        Wallet buyerWallet = walletRepository.findByUserIdUser(buyer.getIdUser())
                .orElseThrow(() -> new EntityNotFoundException("Buyer wallet not found"));

        if (buyerWallet.getIdrBalance().compareTo(totalPrice) < 0) {
            throw new IllegalStateException("Insufficient IDR balance");
        }

        // Deduct/Add balances
        buyerWallet.setIdrBalance(buyerWallet.getIdrBalance().subtract(totalPrice));
        sellerWallet.setIdrBalance(sellerWallet.getIdrBalance().add(totalPrice));
        walletRepository.save(buyerWallet);
        walletRepository.save(sellerWallet);

        String sellerAddress = sellerWallet.getWalletAddress();
        String buyerAddress = buyerWallet.getWalletAddress();

        // Create trade details and transfer tokens
        List<TradeDetail> details = new ArrayList<>();
        for (CarbonToken token : listedTokens) {
            // Transfer ownership
            token.setOwner(buyer);
            token.setStatusToken(TokenStatus.available); // Buyer now holds it available
            tokenRepository.save(token);

            // Create trade detail
            TradeDetail detail = TradeDetail.builder()
                    .transaction(savedTx)
                    .token(token)
                    .hargaToken(listing.getHargaPerToken())
                    .build();
            details.add(tradeDetailRepository.save(detail));
        }

        // Create blockchain transfer entry
        var ledgerEntry = blockchainService.createLedgerEntry(
                BlockchainTxType.transfer,
                savedTx.getIdTransaksi(),
                "trade_transactions",
                BigDecimal.valueOf(request.jumlah()),
                sellerAddress,
                buyerAddress
        );

        savedTx.setTxTransferHash(ledgerEntry.getTxHash());
        transactionRepository.save(savedTx);

        // Update listing quantity
        int remaining = listing.getJumlahToken() - request.jumlah();
        listing.setJumlahToken(remaining);
        if (remaining <= 0) {
            listing.setStatusListing(ListingStatus.soldout);
        }
        listingRepository.save(listing);

        return toTradeResponse(savedTx, details.size());
    }

    public List<TradeResponse> getUserTransactions(int userId) {
        return transactionRepository.findByBuyerIdUserOrSellerIdUserOrderByTanggalTransaksiDesc(userId, userId)
                .stream().map(tx -> {
                    int tokenCount = tradeDetailRepository.findByTransactionIdTransaksi(tx.getIdTransaksi()).size();
                    return toTradeResponse(tx, tokenCount);
                }).collect(Collectors.toList());
    }

    private ListingResponse toListingResponse(Listing l) {
        return new ListingResponse(
                l.getIdListing(),
                l.getProject().getNamaProject(),
                l.getProject().getLokasi(),
                l.getProject().getKategori().getNamaKategori(),
                l.getHargaPerToken(),
                l.getJumlahToken(),
                l.getStatusListing().name(),
                l.getSeller().getIdUser(),
                l.getSeller().getNamaUser(),
                l.getProject().getIdProject(),
                l.getCreatedAt()
        );
    }

    private TradeResponse toTradeResponse(TradeTransaction tx, int tokenCount) {
        return new TradeResponse(
                tx.getIdTransaksi(),
                tx.getListing().getIdListing(),
                tx.getBuyer().getIdUser(),
                tx.getBuyer().getNamaUser(),
                tx.getSeller().getIdUser(),
                tx.getSeller().getNamaUser(),
                tx.getTotalHarga(),
                tx.getMetodeBayar(),
                tx.getStatus().name(),
                tx.getTxTransferHash(),
                tx.getListing().getProject().getNamaProject(),
                tokenCount,
                tx.getTanggalTransaksi()
        );
    }
}
