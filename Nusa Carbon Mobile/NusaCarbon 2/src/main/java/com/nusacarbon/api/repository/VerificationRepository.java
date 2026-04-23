package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.Verification;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface VerificationRepository extends JpaRepository<Verification, Integer> {
    List<Verification> findByMrvReportIdMrv(Integer mrvId);
    Optional<Verification> findTopByMrvReportIdMrvOrderByVerifiedAtDesc(Integer mrvId);
    List<Verification> findByVerifierIdUserOrderByVerifiedAtDesc(Integer verifierId);
}
