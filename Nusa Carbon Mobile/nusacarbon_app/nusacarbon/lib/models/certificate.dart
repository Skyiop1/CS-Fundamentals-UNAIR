class Certificate {
  final int idSertifikat;
  final int idRetirement;
  final String nomorSertifikat; // "CERT-NC-2024-001"
  final String namaEntitas;
  final double totalCo2e;
  final String? linkFilePdf;
  final String? nftTokenId;
  final DateTime createdAt;

  const Certificate({
    required this.idSertifikat,
    required this.idRetirement,
    required this.nomorSertifikat,
    required this.namaEntitas,
    required this.totalCo2e,
    this.linkFilePdf,
    this.nftTokenId,
    required this.createdAt,
  });

  factory Certificate.fromJson(Map<String, dynamic> json) {
    return Certificate(
      idSertifikat: json['id_sertifikat'] as int,
      idRetirement: json['id_retirement'] as int,
      nomorSertifikat: json['nomor_sertifikat'] as String,
      namaEntitas: json['nama_entitas'] as String,
      totalCo2e: (json['total_co2e'] as num).toDouble(),
      linkFilePdf: json['link_file_pdf'] as String?,
      nftTokenId: json['nft_token_id'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_sertifikat': idSertifikat,
      'id_retirement': idRetirement,
      'nomor_sertifikat': nomorSertifikat,
      'nama_entitas': namaEntitas,
      'total_co2e': totalCo2e,
      'link_file_pdf': linkFilePdf,
      'nft_token_id': nftTokenId,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
