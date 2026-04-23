package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.MrvResponse;
import com.nusacarbon.api.dto.MrvSubmitRequest;
import com.nusacarbon.api.service.MrvService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/mrv")
@RequiredArgsConstructor
public class MrvController {

    private final MrvService mrvService;

    @PostMapping("/submit")
    public ResponseEntity<ApiResponse<MrvResponse>> submitMrv(
            @Valid @RequestBody MrvSubmitRequest request) {
        MrvResponse result = mrvService.submitMrvReport(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("MRV report submitted", result));
    }

    @GetMapping("/project/{projectId}")
    public ResponseEntity<ApiResponse<List<MrvResponse>>> getMrvByProject(
            @PathVariable int projectId) {
        List<MrvResponse> reports = mrvService.getMrvByProject(projectId);
        return ResponseEntity.ok(ApiResponse.ok(reports));
    }

    @GetMapping("/pending")
    public ResponseEntity<ApiResponse<List<MrvResponse>>> getPendingMrv() {
        List<MrvResponse> reports = mrvService.getPendingMrvReports();
        return ResponseEntity.ok(ApiResponse.ok(reports));
    }
}
