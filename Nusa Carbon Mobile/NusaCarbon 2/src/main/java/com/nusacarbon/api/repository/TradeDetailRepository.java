package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.TradeDetail;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TradeDetailRepository extends JpaRepository<TradeDetail, Integer> {
    List<TradeDetail> findByTransactionIdTransaksi(Integer transactionId);
}
