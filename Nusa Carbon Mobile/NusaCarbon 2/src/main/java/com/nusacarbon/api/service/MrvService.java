package com.nusacarbon.api.service;

import com.nusacarbon.api.dto.MrvResponse;
import com.nusacarbon.api.dto.MrvSubmitRequest;
import com.nusacarbon.api.entity.MrvReport;
import com.nusacarbon.api.entity.Project;
import com.nusacarbon.api.entity.User;
import com.nusacarbon.api.entity.enums.MrvStatus;
import com.nusacarbon.api.repository.MrvReportRepository;
import com.nusacarbon.api.repository.ProjectRepository;
import com.nusacarbon.api.repository.UserRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class MrvService {

    private final MrvReportRepository mrvReportRepository;
    private final ProjectRepository projectRepository;
    private final UserRepository userRepository;

    @Transactional
    public MrvResponse submitMrvReport(MrvSubmitRequest request) {
        Project project = projectRepository.findById(request.idProject())
                .orElseThrow(() -> new EntityNotFoundException("Project not found"));

        User submitter = userRepository.findById(request.submittedBy())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        MrvReport report = MrvReport.builder()
                .project(project)
                .submittedByUser(submitter)
                .periodeMrv(request.periodeMrv())
                .koordinatGps(request.koordinatGps())
                .linkFotoSatelit(request.linkFotoSatelit())
                .estimasiCo2e(request.estimasiCo2e())
                .catatan(request.catatan())
                .statusMrv(MrvStatus.submitted)
                .build();

        MrvReport saved = mrvReportRepository.save(report);
        return toResponse(saved);
    }

    public List<MrvResponse> getMrvByProject(int projectId) {
        return mrvReportRepository.findByProjectIdProject(projectId)
                .stream().map(this::toResponse).collect(Collectors.toList());
    }

    public List<MrvResponse> getPendingMrvReports() {
        return mrvReportRepository.findByStatusMrv(MrvStatus.submitted)
                .stream().map(this::toResponse).collect(Collectors.toList());
    }

    public MrvReport getMrvEntity(int mrvId) {
        return mrvReportRepository.findById(mrvId)
                .orElseThrow(() -> new EntityNotFoundException("MRV report not found"));
    }

    @Transactional
    public void updateMrvStatus(int mrvId, MrvStatus status) {
        MrvReport report = getMrvEntity(mrvId);
        report.setStatusMrv(status);
        mrvReportRepository.save(report);
    }

    private MrvResponse toResponse(MrvReport m) {
        return new MrvResponse(
                m.getIdMrv(),
                m.getProject().getIdProject(),
                m.getProject().getNamaProject(),
                m.getSubmittedByUser().getIdUser(),
                m.getSubmittedByUser().getNamaUser(),
                m.getPeriodeMrv(),
                m.getKoordinatGps(),
                m.getLinkFotoSatelit(),
                m.getEstimasiCo2e(),
                m.getCatatan(),
                m.getStatusMrv().name(),
                m.getCreatedAt()
        );
    }
}
