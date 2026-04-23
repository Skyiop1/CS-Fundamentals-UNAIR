class VerificationModel {
  final int idVerifikasi;
  final int idMrv;
  final int idVerifier;
  final String hasil; // approved | rejected | revision_needed
  final double? volumeCo2eDisetujui;
  final String? catatanAudit;
  final DateTime verifiedAt;

  const VerificationModel({
    required this.idVerifikasi,
    required this.idMrv,
    required this.idVerifier,
    required this.hasil,
    this.volumeCo2eDisetujui,
    this.catatanAudit,
    required this.verifiedAt,
  });

  factory VerificationModel.fromJson(Map<String, dynamic> json) {
    return VerificationModel(
      idVerifikasi: json['id_verifikasi'] as int,
      idMrv: json['id_mrv'] as int,
      idVerifier: json['id_verifier'] as int,
      hasil: json['hasil'] as String,
      volumeCo2eDisetujui:
          (json['volume_co2e_disetujui'] as num?)?.toDouble(),
      catatanAudit: json['catatan_audit'] as String?,
      verifiedAt: DateTime.parse(json['verified_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_verifikasi': idVerifikasi,
      'id_mrv': idMrv,
      'id_verifier': idVerifier,
      'hasil': hasil,
      'volume_co2e_disetujui': volumeCo2eDisetujui,
      'catatan_audit': catatanAudit,
      'verified_at': verifiedAt.toIso8601String(),
    };
  }
}
