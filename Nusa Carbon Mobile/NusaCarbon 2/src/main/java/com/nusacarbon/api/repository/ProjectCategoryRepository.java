package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.ProjectCategory;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ProjectCategoryRepository extends JpaRepository<ProjectCategory, Integer> {
    Optional<ProjectCategory> findByNamaKategori(String namaKategori);
}
