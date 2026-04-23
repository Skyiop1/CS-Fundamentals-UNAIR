package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.*;
import com.nusacarbon.api.entity.*;
import com.nusacarbon.api.entity.enums.BlockchainTxType;
import com.nusacarbon.api.entity.enums.KycStatus;
import com.nusacarbon.api.repository.*;
import com.nusacarbon.api.service.BlockchainService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class AdminController {

    private final UserRepository userRepository;
    private final WalletRepository walletRepository;
    private final BlockchainService blockchainService;
    private final BlockchainLedgerRepository blockchainLedgerRepository;
    private final VerificationRepository verificationRepository;

    // ---- User endpoints ----

    @GetMapping("/users/{id}")
    public ResponseEntity<ApiResponse<UserResponse>> getUser(@PathVariable int id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("User not found"));
        return ResponseEntity.ok(ApiResponse.ok(toUserResponse(user)));
    }

    @PutMapping("/users/{id}/kyc")
    public ResponseEntity<ApiResponse<UserResponse>> updateKyc(
            @PathVariable int id,
            @Valid @RequestBody KycUpdateRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        KycStatus newStatus = KycStatus.valueOf(request.statusKyc());
        user.setStatusKyc(newStatus);
        User saved = userRepository.save(user);

        return ResponseEntity.ok(ApiResponse.ok("KYC status updated", toUserResponse(saved)));
    }

    @GetMapping("/users")
    public ResponseEntity<ApiResponse<List<UserResponse>>> getAllUsers(
            @RequestParam(required = false) String kycStatus) {
        List<User> users;
        if (kycStatus != null) {
            users = userRepository.findByStatusKyc(KycStatus.valueOf(kycStatus));
        } else {
            users = userRepository.findAll();
        }
        List<UserResponse> responses = users.stream()
                .map(this::toUserResponse).collect(Collectors.toList());
        return ResponseEntity.ok(ApiResponse.ok(responses));
    }

    // ---- Blockchain ledger endpoint ----
    // Supports optional filters: ?userId=, ?projectId=, ?txType=
    // When userId is supplied the ledger is filtered by that user's wallet address.

    @GetMapping("/blockchain/ledger")
    public ResponseEntity<ApiResponse<List<BlockchainTxResponse>>> getLedger(
            @RequestParam(required = false) Integer projectId,
            @RequestParam(required = false) String txType,
            @RequestParam(required = false) Integer userId) {

        List<BlockchainLedger> entries;

        if (userId != null) {
            String walletAddress = walletRepository.findByUserIdUser(userId)
                    .map(Wallet::getWalletAddress)
                    .orElse(null);
            if (walletAddress != null) {
                entries = blockchainLedgerRepository
                        .findByFromAddressOrToAddressOrderByBlockNumberDesc(
                                walletAddress, walletAddress);
            } else {
                entries = List.of();
            }
        } else if (projectId != null) {
            entries = blockchainService.getEntriesByRef(projectId, "carbon_tokens");
        } else if (txType != null) {
            entries = blockchainService.getEntriesByType(BlockchainTxType.valueOf(txType));
        } else {
            entries = blockchainService.getAllEntries();
        }

        List<BlockchainTxResponse> responses = entries.stream()
                .map(this::toLedgerResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(ApiResponse.ok(responses));
    }

    // ---- Verification audit log endpoint ----
    // GET /api/verifications/verifier/{verifierId}
    // Returns all verifications submitted by a given verifier, newest first.

    @GetMapping("/verifications/verifier/{verifierId}")
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> getVerificationsByVerifier(
            @PathVariable int verifierId) {
        List<Map<String, Object>> responses = verificationRepository
                .findByVerifierIdUserOrderByVerifiedAtDesc(verifierId)
                .stream()
                .map(this::toVerificationResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(ApiResponse.ok(responses));
    }

    // ---- Private mapping helpers ----

    private UserResponse toUserResponse(User u) {
        return new UserResponse(
                u.getIdUser(),
                u.getNamaUser(),
                u.getEmail(),
                u.getNoHp(),
                u.getStatusKyc().name(),
                u.getRole() != null ? u.getRole().getRoleName() : null,
                u.getCreatedAt()
        );
    }

    private BlockchainTxResponse toLedgerResponse(BlockchainLedger l) {
        return new BlockchainTxResponse(
                l.getTxHash(),
                l.getPrevHash(),
                l.getTxType().name(),
                l.getAmountCo2e(),
                l.getFromAddress(),
                l.getToAddress(),
                l.getGasFeeMock(),
                l.getBlockNumber(),
                l.getRefId(),
                l.getRefTable(),
                l.getCreatedAt()
        );
    }

    // Uses LinkedHashMap so null fields are preserved (unlike Map.of which rejects nulls).
    private Map<String, Object> toVerificationResponse(Verification v) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id_verifikasi", v.getIdVerifikasi());
        map.put("id_mrv", v.getMrvReport().getIdMrv());
        map.put("id_verifier", v.getVerifier().getIdUser());
        map.put("hasil", v.getHasil().name());
        map.put("volume_co2e_disetujui", v.getVolumeCo2eDisetujui());
        map.put("catatan_audit", v.getCatatanAudit());
        map.put("verified_at", v.getVerifiedAt().toString());
        return map;
    }
}
