package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.DocumentType;
import com.nusacarbon.api.entity.enums.DocumentVerificationStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "project_documents")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProjectDocument {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idDokumen;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_project", nullable = false)
    private Project project;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "uploaded_by", nullable = false)
    private User uploadedBy;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private DocumentType tipeDokumen;

    @Column(nullable = false, length = 500)
    private String filePath;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private DocumentVerificationStatus statusVerifikasi = DocumentVerificationStatus.pending;

    @Column(columnDefinition = "TEXT")
    private String catatanVerifikasi;

    private LocalDateTime verifiedAt;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
