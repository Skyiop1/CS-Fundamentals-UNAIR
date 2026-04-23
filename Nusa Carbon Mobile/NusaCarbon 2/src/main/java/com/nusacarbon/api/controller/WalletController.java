package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.WalletResponse;
import com.nusacarbon.api.service.WalletService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/wallet")
@RequiredArgsConstructor
public class WalletController {

    private final WalletService walletService;

    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<WalletResponse>> getWallet(@PathVariable int userId) {
        WalletResponse wallet = walletService.getWalletByUserId(userId);
        return ResponseEntity.ok(ApiResponse.ok(wallet));
    }
}
