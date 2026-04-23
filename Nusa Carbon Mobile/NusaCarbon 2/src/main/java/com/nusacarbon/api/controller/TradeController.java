package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.TradeRequest;
import com.nusacarbon.api.dto.TradeResponse;
import com.nusacarbon.api.service.TradeService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@RequiredArgsConstructor
public class TradeController {

    private final TradeService tradeService;

    @PostMapping("/buy")
    public ResponseEntity<ApiResponse<TradeResponse>> buyTokens(
            @Valid @RequestBody TradeRequest request) {
        TradeResponse trade = tradeService.executeTrade(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Trade executed successfully", trade));
    }

    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<List<TradeResponse>>> getUserTransactions(
            @PathVariable int userId) {
        List<TradeResponse> transactions = tradeService.getUserTransactions(userId);
        return ResponseEntity.ok(ApiResponse.ok(transactions));
    }
}
