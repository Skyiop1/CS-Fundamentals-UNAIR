package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.ListingStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "listings")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Listing {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idListing;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_user", nullable = false)
    private User seller;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_project", nullable = false)
    private Project project;

    @Column(nullable = false, precision = 14, scale = 2)
    private BigDecimal hargaPerToken;

    @Column(nullable = false)
    private Integer jumlahToken;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private ListingStatus statusListing = ListingStatus.active;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
