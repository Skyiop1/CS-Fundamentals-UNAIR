package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.BlockchainLedger;
import com.nusacarbon.api.entity.enums.BlockchainTxType;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface BlockchainLedgerRepository extends JpaRepository<BlockchainLedger, Integer> {
    Optional<BlockchainLedger> findTopByOrderByBlockNumberDesc();
    List<BlockchainLedger> findByRefIdAndRefTable(Integer refId, String refTable);
    List<BlockchainLedger> findByTxType(BlockchainTxType txType);
    List<BlockchainLedger> findAllByOrderByBlockNumberAsc();
    List<BlockchainLedger> findByFromAddressOrToAddressOrderByBlockNumberDesc(
            String fromAddress, String toAddress);
}
