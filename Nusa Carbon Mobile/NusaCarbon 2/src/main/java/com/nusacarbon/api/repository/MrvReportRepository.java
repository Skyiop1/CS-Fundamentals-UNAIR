package com.nusacarbon.api.repository;

import com.nusacarbon.api.entity.MrvReport;
import com.nusacarbon.api.entity.enums.MrvStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MrvReportRepository extends JpaRepository<MrvReport, Integer> {
    List<MrvReport> findByProjectIdProject(Integer projectId);
    List<MrvReport> findByStatusMrv(MrvStatus status);
}
