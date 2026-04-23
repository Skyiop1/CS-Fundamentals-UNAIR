class Retirement {
  final int idRetirement;
  final int idUser;
  final double totalCo2e;
  final String? alasan; // CSR, regulasi, etc.
  final String? namaEntitas; // Company/individual name on certificate
  final String status; // pending | completed | failed
  final DateTime createdAt;

  const Retirement({
    required this.idRetirement,
    required this.idUser,
    required this.totalCo2e,
    this.alasan,
    this.namaEntitas,
    required this.status,
    required this.createdAt,
  });

  factory Retirement.fromJson(Map<String, dynamic> json) {
    return Retirement(
      idRetirement: json['id_retirement'] as int,
      idUser: json['id_user'] as int,
      totalCo2e: (json['total_co2e'] as num).toDouble(),
      alasan: json['alasan'] as String?,
      namaEntitas: json['nama_entitas'] as String?,
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_retirement': idRetirement,
      'id_user': idUser,
      'total_co2e': totalCo2e,
      'alasan': alasan,
      'nama_entitas': namaEntitas,
      'status': status,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
