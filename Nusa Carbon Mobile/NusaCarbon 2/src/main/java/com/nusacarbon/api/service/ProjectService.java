package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.ProjectRequest;
import com.nusacarbon.api.dto.ProjectResponse;
import com.nusacarbon.api.entity.Project;
import com.nusacarbon.api.entity.ProjectCategory;
import com.nusacarbon.api.entity.User;
import com.nusacarbon.api.entity.enums.ProjectStatus;
import com.nusacarbon.api.repository.ProjectCategoryRepository;
import com.nusacarbon.api.repository.ProjectRepository;
import com.nusacarbon.api.repository.UserRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ProjectService {

    private final ProjectRepository projectRepository;
    private final UserRepository userRepository;
    private final ProjectCategoryRepository categoryRepository;

    /**
     * Retrieves projects with optional filters.
     *
     * @param status   project status string (e.g. "verified", "submitted")
     * @param kategori category name string (e.g. "Hutan", "Mangrove")
     */
    public List<ProjectResponse> getAllProjects(String status, String kategori) {
        List<Project> projects;

        ProjectStatus projectStatus = null;
        if (status != null && !status.isBlank()) {
            projectStatus = ProjectStatus.valueOf(status);
        }

        if (projectStatus != null && kategori != null && !kategori.isBlank()) {
            projects = projectRepository.findByStatusProjectAndKategoriNamaKategori(
                    projectStatus, kategori);
        } else if (projectStatus != null) {
            projects = projectRepository.findByStatusProject(projectStatus);
        } else if (kategori != null && !kategori.isBlank()) {
            projects = projectRepository.findByKategoriNamaKategori(kategori);
        } else {
            projects = projectRepository.findAll();
        }

        return projects.stream().map(this::toResponse).collect(Collectors.toList());
    }

    public ProjectResponse getProjectById(int id) {
        Project project = projectRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Project not found with id: " + id));
        return toResponse(project);
    }

    @Transactional
    public ProjectResponse createProject(ProjectRequest request) {
        User user = userRepository.findById(request.idUser())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));
        ProjectCategory category = categoryRepository.findById(request.idKategori())
                .orElseThrow(() -> new EntityNotFoundException("Category not found"));

        Project project = Project.builder()
                .user(user)
                .kategori(category)
                .namaProject(request.namaProject())
                .lokasi(request.lokasi())
                .koordinatLat(request.koordinatLat())
                .koordinatLng(request.koordinatLng())
                .luasLahan(request.luasLahan())
                .deskripsi(request.deskripsi())
                .statusProject(ProjectStatus.submitted)
                .build();

        Project saved = projectRepository.save(project);
        return toResponse(saved);
    }

    private ProjectResponse toResponse(Project p) {
        return new ProjectResponse(
                p.getIdProject(),
                p.getNamaProject(),
                p.getLokasi(),
                p.getKategori().getNamaKategori(),
                p.getStatusProject().name(),
                p.getLuasLahan(),
                p.getKoordinatLat(),
                p.getKoordinatLng(),
                p.getDeskripsi(),
                p.getImageUrl(),
                p.getUser().getIdUser(),
                p.getUser().getNamaUser(),
                p.getCreatedAt(),
                p.getUpdatedAt()
        );
    }
}
