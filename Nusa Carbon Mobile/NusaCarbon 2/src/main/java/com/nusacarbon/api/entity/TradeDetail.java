package com.nusacarbon.api.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "trade_details")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TradeDetail {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idDetail;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_transaksi", nullable = false)
    private TradeTransaction transaction;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_token", nullable = false)
    private CarbonToken token;

    @Column(nullable = false, precision = 14, scale = 2)
    private BigDecimal hargaToken;
}
