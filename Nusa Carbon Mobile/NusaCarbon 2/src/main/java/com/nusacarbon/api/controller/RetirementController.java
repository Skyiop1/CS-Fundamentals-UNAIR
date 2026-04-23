package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.RetirementRequest;
import com.nusacarbon.api.dto.RetirementResponse;
import com.nusacarbon.api.service.RetirementService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/retirements")
@RequiredArgsConstructor
public class RetirementController {

    private final RetirementService retirementService;

    @PostMapping
    public ResponseEntity<ApiResponse<RetirementResponse>> retireTokens(
            @Valid @RequestBody RetirementRequest request) {
        RetirementResponse result = retirementService.retireTokens(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Tokens retired successfully. Certificate generated.", result));
    }

    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<List<RetirementResponse>>> getUserRetirements(
            @PathVariable int userId) {
        List<RetirementResponse> retirements = retirementService.getUserRetirements(userId);
        return ResponseEntity.ok(ApiResponse.ok(retirements));
    }
}
