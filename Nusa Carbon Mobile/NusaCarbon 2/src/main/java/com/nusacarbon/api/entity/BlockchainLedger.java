package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.BlockchainTxType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "blockchain_ledger")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BlockchainLedger {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private Integer blockNumber;

    @Column(nullable = false, unique = true, length = 66)
    private String txHash;

    @Column(nullable = false, length = 66)
    private String prevHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private BlockchainTxType txType;

    @Column(nullable = false)
    private Integer refId;

    @Column(nullable = false, length = 50)
    private String refTable;

    @Column(nullable = false, precision = 14, scale = 4)
    private BigDecimal amountCo2e;

    @Column(length = 100)
    private String fromAddress;

    @Column(length = 100)
    private String toAddress;

    @Column(precision = 8, scale = 6)
    @Builder.Default
    private BigDecimal gasFeeMock = new BigDecimal("0.004000");

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;

    // Append-only: NO @PreUpdate or @PreRemove
    // Enforcement is in the service layer
}
