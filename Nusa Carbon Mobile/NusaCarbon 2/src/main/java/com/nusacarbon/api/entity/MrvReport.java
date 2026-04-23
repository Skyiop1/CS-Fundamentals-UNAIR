package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.MrvStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "mrv_reports")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MrvReport {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idMrv;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_project", nullable = false)
    private Project project;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "submitted_by", nullable = false)
    private User submittedByUser;

    @Column(nullable = false, length = 50)
    private String periodeMrv;

    @Column(columnDefinition = "TEXT")
    private String koordinatGps;

    @Column(length = 500)
    private String linkFotoSatelit;

    @Column(precision = 14, scale = 4)
    private BigDecimal estimasiCo2e;

    @Column(columnDefinition = "TEXT")
    private String catatan;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private MrvStatus statusMrv = MrvStatus.submitted;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
