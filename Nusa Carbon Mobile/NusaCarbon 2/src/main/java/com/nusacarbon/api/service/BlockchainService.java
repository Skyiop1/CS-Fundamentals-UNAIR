package com.nusacarbon.api.service;

import com.nusacarbon.api.entity.BlockchainLedger;
import com.nusacarbon.api.entity.enums.BlockchainTxType;
import com.nusacarbon.api.repository.BlockchainLedgerRepository;
import com.nusacarbon.api.util.BlockchainHashUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class BlockchainService {

    private final BlockchainLedgerRepository ledgerRepository;

    /**
     * Create a new blockchain ledger entry. NEVER update or delete.
     */
    @Transactional
    public BlockchainLedger createLedgerEntry(
            BlockchainTxType txType,
            int refId,
            String refTable,
            BigDecimal amountCo2e,
            String fromAddress,
            String toAddress
    ) {
        String prevHash = BlockchainHashUtil.getPreviousHash(ledgerRepository);
        int lastBlock = BlockchainHashUtil.getLastBlockNumber(ledgerRepository);
        String timestamp = LocalDateTime.now().toString();

        String txHash = BlockchainHashUtil.generateTxHash(
                prevHash,
                txType.name(),
                amountCo2e.doubleValue(),
                refId,
                timestamp
        );

        BlockchainLedger entry = BlockchainLedger.builder()
                .blockNumber(lastBlock + 1)
                .txHash(txHash)
                .prevHash(prevHash)
                .txType(txType)
                .refId(refId)
                .refTable(refTable)
                .amountCo2e(amountCo2e)
                .fromAddress(fromAddress)
                .toAddress(toAddress)
                .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee()))
                .build();

        return ledgerRepository.save(entry);
    }

    public List<BlockchainLedger> getAllEntries() {
        return ledgerRepository.findAllByOrderByBlockNumberAsc();
    }

    public List<BlockchainLedger> getEntriesByRef(int refId, String refTable) {
        return ledgerRepository.findByRefIdAndRefTable(refId, refTable);
    }

    public List<BlockchainLedger> getEntriesByType(BlockchainTxType txType) {
        return ledgerRepository.findByTxType(txType);
    }
}
