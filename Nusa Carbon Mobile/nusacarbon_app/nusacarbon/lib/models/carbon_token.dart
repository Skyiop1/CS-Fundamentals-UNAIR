class CarbonToken {
  final int idToken;
  final int idProject;
  final int idVerifikasi;
  final int ownerUserId;
  final String tokenSerial; // "NC-2024-001-000001"
  final int vintageYear;
  final String statusToken; // available | listed | sold | retired
  final String? txMintHash; // blockchain tx hash
  final String? metadataHash;
  final DateTime createdAt;
  // Derived fields
  final String namaProject;
  final String lokasi;
  final String namaKategori;
  final String? imageUrl;
  final double? amount; // aggregated tCO₂e for display

  const CarbonToken({
    required this.idToken,
    required this.idProject,
    required this.idVerifikasi,
    required this.ownerUserId,
    required this.tokenSerial,
    required this.vintageYear,
    required this.statusToken,
    this.txMintHash,
    this.metadataHash,
    required this.createdAt,
    required this.namaProject,
    required this.lokasi,
    required this.namaKategori,
    this.imageUrl,
    this.amount,
  });

  factory CarbonToken.fromJson(Map<String, dynamic> json) {
    return CarbonToken(
      idToken: (json['id_token'] as num?)?.toInt() ?? 0,
      idProject: (json['id_project'] as num?)?.toInt() ?? 0,
      idVerifikasi: (json['id_verifikasi'] as num?)?.toInt() ?? 0,
      ownerUserId: (json['owner_user_id'] as num?)?.toInt() ?? 0,
      tokenSerial: json['token_serial']?.toString() ?? '',
      vintageYear: (json['vintage_year'] as num?)?.toInt() ?? 0,
      statusToken: json['status_token']?.toString() ?? 'available',
      txMintHash: json['tx_mint_hash']?.toString(),
      metadataHash: json['metadata_hash']?.toString(),
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ?? DateTime.now(),
      namaProject: json['nama_project']?.toString() ?? '',
      lokasi: json['lokasi']?.toString() ?? '',
      namaKategori: json['nama_kategori']?.toString() ?? '',
      imageUrl: json['image_url']?.toString(),
      amount: (json['amount'] as num?)?.toDouble() ?? 1.0, // Fallback to 1.0 tCO2e
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_token': idToken,
      'id_project': idProject,
      'id_verifikasi': idVerifikasi,
      'owner_user_id': ownerUserId,
      'token_serial': tokenSerial,
      'vintage_year': vintageYear,
      'status_token': statusToken,
      'tx_mint_hash': txMintHash,
      'metadata_hash': metadataHash,
      'created_at': createdAt.toIso8601String(),
      'nama_project': namaProject,
      'lokasi': lokasi,
      'nama_kategori': namaKategori,
      'image_url': imageUrl,
      'amount': amount,
    };
  }
}
