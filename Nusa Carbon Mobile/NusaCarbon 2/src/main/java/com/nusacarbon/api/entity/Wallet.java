package com.nusacarbon.api.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "wallets")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Wallet {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idWallet;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_user", unique = true, nullable = false)
    private User user;

    @Column(nullable = false, unique = true, length = 255)
    private String walletAddress;

    @Column(length = 50)
    @Builder.Default
    private String chainNetwork = "ethereum";

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;
}
