package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.ProjectStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "projects")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idProject;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_user", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_kategori", nullable = false)
    private ProjectCategory kategori;

    @Column(nullable = false, length = 200)
    private String namaProject;

    @Column(nullable = false, length = 255)
    private String lokasi;

    @Column(precision = 10, scale = 7)
    private BigDecimal koordinatLat;

    @Column(precision = 10, scale = 7)
    private BigDecimal koordinatLng;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal luasLahan;

    @Column(columnDefinition = "TEXT")
    private String deskripsi;

    @Column(length = 500)
    private String imageUrl;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private ProjectStatus statusProject = ProjectStatus.draft;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;
}
