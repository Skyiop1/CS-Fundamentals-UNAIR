package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.Certificate;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CertificateRepository extends JpaRepository<Certificate, Integer> {
    Optional<Certificate> findByRetirementIdRetirement(Integer retirementId);
}
