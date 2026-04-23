package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.TradeTransaction;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TradeTransactionRepository extends JpaRepository<TradeTransaction, Integer> {
    List<TradeTransaction> findByBuyerIdUserOrderByTanggalTransaksiDesc(Integer buyerId);
    List<TradeTransaction> findBySellerIdUserOrderByTanggalTransaksiDesc(Integer sellerId);
    List<TradeTransaction> findByBuyerIdUserOrSellerIdUserOrderByTanggalTransaksiDesc(Integer buyerId, Integer sellerId);
}
