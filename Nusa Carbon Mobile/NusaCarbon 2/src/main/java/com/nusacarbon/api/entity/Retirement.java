package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.RetirementStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "retirements")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Retirement {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idRetirement;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_user", nullable = false)
    private User user;

    @Column(nullable = false, precision = 14, scale = 4)
    private BigDecimal totalCo2e;

    @Column(columnDefinition = "TEXT")
    private String alasan;

    @Column(length = 200)
    private String namaEntitas;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private RetirementStatus status = RetirementStatus.pending;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
