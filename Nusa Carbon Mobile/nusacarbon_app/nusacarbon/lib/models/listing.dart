class Listing {
  final int idListing;
  final int idUser; // Seller
  final int idProject;
  final double hargaPerToken; // IDR
  final int jumlahToken;
  final String statusListing; // active | soldout | closed
  final DateTime createdAt;
  // Derived
  final String namaProject;
  final String sellerName;
  final String? namaKategori;
  final String? lokasi;
  final String? imageUrl;

  const Listing({
    required this.idListing,
    required this.idUser,
    required this.idProject,
    required this.hargaPerToken,
    required this.jumlahToken,
    required this.statusListing,
    required this.createdAt,
    required this.namaProject,
    required this.sellerName,
    this.namaKategori,
    this.lokasi,
    this.imageUrl,
  });

  factory Listing.fromJson(Map<String, dynamic> json) {
    return Listing(
      idListing: (json['id_listing'] as num?)?.toInt() ?? 0,
      idUser: ((json['seller_user_id'] ?? json['id_user']) as num?)?.toInt() ?? 0,
      idProject: (json['id_project'] as num?)?.toInt() ?? 0,
      hargaPerToken: (json['harga_per_token'] as num?)?.toDouble() ?? 0.0,
      jumlahToken: (json['jumlah_token'] as num?)?.toInt() ?? 0,
      statusListing: json['status_listing']?.toString() ?? 'active',
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ?? DateTime.now(),
      namaProject: json['nama_project']?.toString() ?? '',
      sellerName: json['seller_name']?.toString() ?? '',
      namaKategori: json['nama_kategori']?.toString(),
      lokasi: json['lokasi']?.toString(),
      imageUrl: json['image_url']?.toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_listing': idListing,
      'id_user': idUser,
      'id_project': idProject,
      'harga_per_token': hargaPerToken,
      'jumlah_token': jumlahToken,
      'status_listing': statusListing,
      'created_at': createdAt.toIso8601String(),
      'nama_project': namaProject,
      'seller_name': sellerName,
      'nama_kategori': namaKategori,
      'lokasi': lokasi,
      'image_url': imageUrl,
    };
  }
}
