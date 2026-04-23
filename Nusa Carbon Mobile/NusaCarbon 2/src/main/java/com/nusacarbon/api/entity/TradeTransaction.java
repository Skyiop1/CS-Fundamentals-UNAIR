package com.nusacarbon.api.entity;

import com.nusacarbon.api.entity.enums.TxStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "trade_transactions")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TradeTransaction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idTransaksi;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_listing", nullable = false)
    private Listing listing;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "buyer_user_id", nullable = false)
    private User buyer;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "seller_user_id", nullable = false)
    private User seller;

    @Column(nullable = false, precision = 16, scale = 2)
    private BigDecimal totalHarga;

    @Column(nullable = false, length = 50)
    private String metodeBayar;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private TxStatus status = TxStatus.pending;

    @Column(length = 255)
    private String txTransferHash;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime tanggalTransaksi;
}
