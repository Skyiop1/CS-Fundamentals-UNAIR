package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.User;
import com.nusacarbon.api.entity.enums.KycStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Integer> {
    Optional<User> findByEmail(String email);
    List<User> findByStatusKyc(KycStatus status);
}
