package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.ListingRequest;
import com.nusacarbon.api.dto.ListingResponse;
import com.nusacarbon.api.service.TradeService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/listings")
@RequiredArgsConstructor
public class MarketplaceController {

    private final TradeService tradeService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<ListingResponse>>> getActiveListings(
            @RequestParam(required = false) String kategori) {
        List<ListingResponse> listings = tradeService.getActiveListings(kategori);
        return ResponseEntity.ok(ApiResponse.ok(listings));
    }

    @PostMapping
    public ResponseEntity<ApiResponse<ListingResponse>> createListing(
            @Valid @RequestBody ListingRequest request) {
        ListingResponse listing = tradeService.createListing(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Listing created successfully", listing));
    }
}
