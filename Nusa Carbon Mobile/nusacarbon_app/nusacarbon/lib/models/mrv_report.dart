class MrvReport {
  final int idMrv;
  final int idProject;
  final int submittedBy;
  final String periodeMrv; // "2024-Q1"
  final String? koordinatGps; // JSON array
  final String? linkFotoSatelit;
  final double? estimasiCo2e;
  final String? catatan;
  final String statusMrv; // submitted | under_review | reviewed | revision_needed
  final DateTime createdAt;
  // Derived / joined fields returned by the API
  final String? namaProject;
  final String? submitterName;

  const MrvReport({
    required this.idMrv,
    required this.idProject,
    required this.submittedBy,
    required this.periodeMrv,
    this.koordinatGps,
    this.linkFotoSatelit,
    this.estimasiCo2e,
    this.catatan,
    required this.statusMrv,
    required this.createdAt,
    this.namaProject,
    this.submitterName,
  });

  factory MrvReport.fromJson(Map<String, dynamic> json) {
    return MrvReport(
      idMrv: json['id_mrv'] as int,
      idProject: json['id_project'] as int,
      submittedBy: (json['submitted_by'] as num).toInt(),
      periodeMrv: json['periode_mrv'] as String,
      koordinatGps: json['koordinat_gps'] as String?,
      linkFotoSatelit: json['link_foto_satelit'] as String?,
      estimasiCo2e: (json['estimasi_co2e'] as num?)?.toDouble(),
      catatan: json['catatan'] as String?,
      statusMrv: json['status_mrv'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      namaProject: json['nama_project'] as String?,
      submitterName: json['submitter_name'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_mrv': idMrv,
      'id_project': idProject,
      'submitted_by': submittedBy,
      'periode_mrv': periodeMrv,
      'koordinat_gps': koordinatGps,
      'link_foto_satelit': linkFotoSatelit,
      'estimasi_co2e': estimasiCo2e,
      'catatan': catatan,
      'status_mrv': statusMrv,
      'created_at': createdAt.toIso8601String(),
      'nama_project': namaProject,
      'submitter_name': submitterName,
    };
  }
}
