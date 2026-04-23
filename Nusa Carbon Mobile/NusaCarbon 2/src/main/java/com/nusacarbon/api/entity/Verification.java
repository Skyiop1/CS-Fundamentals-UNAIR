package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.VerificationResult;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "verifications")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Verification {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idVerifikasi;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_mrv", nullable = false)
    private MrvReport mrvReport;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_verifier", nullable = false)
    private User verifier;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private VerificationResult hasil;

    @Column(precision = 14, scale = 4)
    private BigDecimal volumeCo2eDisetujui;

    @Column(columnDefinition = "TEXT")
    private String catatanAudit;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime verifiedAt;
}
