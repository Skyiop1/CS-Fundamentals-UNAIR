package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.TokenStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "carbon_tokens")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CarbonToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idToken;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_project", nullable = false)
    private Project project;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_verifikasi", nullable = false)
    private Verification verification;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "owner_user_id", nullable = false)
    private User owner;

    @Column(nullable = false, unique = true, length = 100)
    private String tokenSerial;

    @Column(nullable = false)
    private Integer vintageYear;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private TokenStatus statusToken = TokenStatus.available;

    @Column(length = 255)
    private String txMintHash;

    @Column(length = 255)
    private String metadataHash;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
