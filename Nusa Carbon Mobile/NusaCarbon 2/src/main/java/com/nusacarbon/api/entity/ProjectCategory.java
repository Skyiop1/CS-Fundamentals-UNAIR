package com.nusacarbon.api.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "project_categories")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProjectCategory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idKategori;

    @Column(nullable = false, unique = true, length = 100)
    private String namaKategori;

    @Column(columnDefinition = "TEXT")
    private String deskripsi;
}
