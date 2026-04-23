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
      idListing: json['id_listing'] as int,
      idUser: (json['seller_user_id'] ?? json['id_user']) as int,
      idProject: json['id_project'] as int,
      hargaPerToken: (json['harga_per_token'] as num).toDouble(),
      jumlahToken: json['jumlah_token'] as int,
      statusListing: json['status_listing'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      namaProject: json['nama_project'] as String? ?? '',
      sellerName: json['seller_name'] as String? ?? '',
      namaKategori: json['nama_kategori'] as String?,
      lokasi: json['lokasi'] as String?,
      imageUrl: json['image_url'] as String?,
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
