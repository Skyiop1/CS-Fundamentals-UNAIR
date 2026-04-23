package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.RetirementDetail;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RetirementDetailRepository extends JpaRepository<RetirementDetail, Integer> {
    List<RetirementDetail> findByRetirementIdRetirement(Integer retirementId);
}
