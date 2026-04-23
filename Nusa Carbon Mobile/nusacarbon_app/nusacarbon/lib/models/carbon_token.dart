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
      idToken: json['id_token'] as int,
      idProject: json['id_project'] as int,
      idVerifikasi: json['id_verifikasi'] as int,
      ownerUserId: json['owner_user_id'] as int,
      tokenSerial: json['token_serial'] as String,
      vintageYear: json['vintage_year'] as int,
      statusToken: json['status_token'] as String,
      txMintHash: json['tx_mint_hash'] as String?,
      metadataHash: json['metadata_hash'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      namaProject: json['nama_project'] as String? ?? '',
      lokasi: json['lokasi'] as String? ?? '',
      namaKategori: json['nama_kategori'] as String? ?? '',
      imageUrl: json['image_url'] as String?,
      amount: (json['amount'] as num?)?.toDouble(),
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
