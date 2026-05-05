package com.nusacarbon.api.controller;

import com.nusacarbon.api.dto.ApiResponse;
import com.nusacarbon.api.dto.ProjectRequest;
import com.nusacarbon.api.dto.ProjectResponse;
import com.nusacarbon.api.service.ProjectService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/projects")
@RequiredArgsConstructor
public class ProjectController {

    private final ProjectService projectService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<ProjectResponse>>> getAllProjects(
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String kategori) {
        List<ProjectResponse> projects = projectService.getAllProjects(status, kategori);
        return ResponseEntity.ok(ApiResponse.ok(projects));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<ProjectResponse>> getProjectById(@PathVariable int id) {
        ProjectResponse project = projectService.getProjectById(id);
        return ResponseEntity.ok(ApiResponse.ok(project));
    }

    @PostMapping
    public ResponseEntity<ApiResponse<ProjectResponse>> createProject(
            @Valid @RequestBody ProjectRequest request) {
        ProjectResponse project = projectService.createProject(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Project submitted successfully", project));
    }
}
