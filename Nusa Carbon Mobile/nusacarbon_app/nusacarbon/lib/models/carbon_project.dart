class CarbonProject {
  final int idProject;
  final int idUser; // Project owner
  final int idKategori;
  final String namaProject;
  final String lokasi;
  final double? koordinatLat;
  final double? koordinatLng;
  final double luasLahan; // hectares
  final String? deskripsi;
  final String statusProject; // draft | submitted | verified | rejected
  final DateTime createdAt;
  final DateTime? updatedAt;
  // Derived/joined fields returned by the API
  final String namaKategori; // from project_categories join
  final String? ownerName; // from users join (ProjectResponse.ownerName)
  final String? imageUrl;

  const CarbonProject({
    required this.idProject,
    required this.idUser,
    this.idKategori = 0,
    required this.namaProject,
    required this.lokasi,
    this.koordinatLat,
    this.koordinatLng,
    required this.luasLahan,
    this.deskripsi,
    required this.statusProject,
    required this.createdAt,
    this.updatedAt,
    required this.namaKategori,
    this.ownerName,
    this.imageUrl,
  });

  factory CarbonProject.fromJson(Map<String, dynamic> json) {
    return CarbonProject(
      idProject: (json['id_project'] as num?)?.toInt() ?? 0,
      idUser: (json['id_user'] as num?)?.toInt() ?? 0,
      idKategori: (json['id_kategori'] as num?)?.toInt() ?? 0,
      namaProject: json['nama_project']?.toString() ?? '',
      lokasi: json['lokasi']?.toString() ?? '',
      koordinatLat: (json['koordinat_lat'] as num?)?.toDouble(),
      koordinatLng: (json['koordinat_lng'] as num?)?.toDouble(),
      luasLahan: (json['luas_lahan'] as num?)?.toDouble() ?? 0.0,
      deskripsi: json['deskripsi']?.toString(),
      statusProject: json['status_project']?.toString() ?? 'draft',
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ?? DateTime.now(),
      updatedAt: json['updated_at'] != null ? DateTime.tryParse(json['updated_at'].toString()) : null,
      namaKategori: json['nama_kategori']?.toString() ?? '',
      ownerName: json['owner_name']?.toString(),
      imageUrl: json['image_url']?.toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_project': idProject,
      'id_user': idUser,
      'id_kategori': idKategori,
      'nama_project': namaProject,
      'lokasi': lokasi,
      'koordinat_lat': koordinatLat,
      'koordinat_lng': koordinatLng,
      'luas_lahan': luasLahan,
      'deskripsi': deskripsi,
      'status_project': statusProject,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'nama_kategori': namaKategori,
      'owner_name': ownerName,
      'image_url': imageUrl,
    };
  }
}
