package com.nusacarbon.api.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "certificates")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Certificate {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idSertifikat;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_retirement", unique = true, nullable = false)
    private Retirement retirement;

    @Column(nullable = false, unique = true, length = 100)
    private String nomorSertifikat;

    @Column(nullable = false, length = 200)
    private String namaEntitas;

    @Column(nullable = false, precision = 14, scale = 4)
    private BigDecimal totalCo2e;

    @Column(length = 500)
    private String linkFilePdf;

    @Column(length = 255)
    private String nftTokenId;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
