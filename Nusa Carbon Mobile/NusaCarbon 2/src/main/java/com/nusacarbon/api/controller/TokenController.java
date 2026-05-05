package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.MintRequest;
import com.nusacarbon.api.dto.TokenResponse;
import com.nusacarbon.api.service.TokenService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tokens")
@RequiredArgsConstructor
public class TokenController {

    private final TokenService tokenService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<TokenResponse>>> getTokens(
            @RequestParam(required = false) Integer ownerId,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) Integer vintage) {
        List<TokenResponse> tokens = tokenService.getTokens(ownerId, status, vintage);
        return ResponseEntity.ok(ApiResponse.ok(tokens));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<TokenResponse>> getTokenById(@PathVariable int id) {
        TokenResponse token = tokenService.getTokenById(id);
        return ResponseEntity.ok(ApiResponse.ok(token));
    }

    @PostMapping("/mint")
    public ResponseEntity<ApiResponse<List<TokenResponse>>> mintTokens(
            @Valid @RequestBody MintRequest request) {
        List<TokenResponse> minted = tokenService.mintTokens(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Tokens minted successfully", minted));
    }
}
