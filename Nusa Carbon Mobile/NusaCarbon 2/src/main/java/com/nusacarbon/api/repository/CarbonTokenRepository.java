package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.CarbonToken;
import com.nusacarbon.api.entity.enums.TokenStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CarbonTokenRepository extends JpaRepository<CarbonToken, Integer> {
    List<CarbonToken> findByOwnerIdUser(Integer userId);
    List<CarbonToken> findByOwnerIdUserAndStatusToken(Integer userId, TokenStatus status);
    List<CarbonToken> findByStatusToken(TokenStatus status);
    List<CarbonToken> findByProjectIdProject(Integer projectId);
    List<CarbonToken> findByVintageYear(Integer year);
    List<CarbonToken> findByOwnerIdUserAndStatusTokenAndVintageYear(Integer userId, TokenStatus status, Integer year);
    long countByOwnerIdUser(Integer userId);
    long countByOwnerIdUserAndStatusToken(Integer userId, TokenStatus status);
}
