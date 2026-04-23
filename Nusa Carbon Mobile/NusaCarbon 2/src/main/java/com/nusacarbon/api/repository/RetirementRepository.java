package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.Retirement;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RetirementRepository extends JpaRepository<Retirement, Integer> {
    List<Retirement> findByUserIdUserOrderByCreatedAtDesc(Integer userId);
}
