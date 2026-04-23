package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.Wallet;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface WalletRepository extends JpaRepository<Wallet, Integer> {
    Optional<Wallet> findByUserIdUser(Integer userId);
}
