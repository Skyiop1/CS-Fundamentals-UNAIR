package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.ProjectDocument;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProjectDocumentRepository extends JpaRepository<ProjectDocument, Integer> {
    List<ProjectDocument> findByProjectIdProject(Integer projectId);
}
