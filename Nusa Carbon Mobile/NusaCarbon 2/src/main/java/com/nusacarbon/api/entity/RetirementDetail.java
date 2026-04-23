package com.nusacarbon.api.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "retirement_details")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RetirementDetail {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idDetailRetirement;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_retirement", nullable = false)
    private Retirement retirement;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_token", nullable = false)
    private CarbonToken token;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime retiredAt;
}
