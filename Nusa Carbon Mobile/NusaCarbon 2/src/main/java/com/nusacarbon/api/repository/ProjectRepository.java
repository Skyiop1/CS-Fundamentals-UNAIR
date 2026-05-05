package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.Project;
import com.nusacarbon.api.entity.enums.ProjectStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProjectRepository extends JpaRepository<Project, Integer> {
    List<Project> findByStatusProject(ProjectStatus status);
    List<Project> findByKategoriIdKategori(Integer kategoriId);
    List<Project> findByStatusProjectAndKategoriIdKategori(ProjectStatus status, Integer kategoriId);
    List<Project> findByUserIdUser(Integer userId);

    // Filter by category name (for Flutter marketplace filter)
    List<Project> findByKategoriNamaKategori(String namaKategori);
    List<Project> findByStatusProjectAndKategoriNamaKategori(ProjectStatus status, String namaKategori);
}
