class TradeTransaction {
  final int idTransaksi;
  final int idListing;
  final int buyerUserId;
  final int sellerUserId;
  final double totalHarga; // IDR
  final String metodeBayar; // crypto | transfer_bank
  final String status; // pending | paid | failed | success
  final String? txTransferHash;
  final DateTime tanggalTransaksi;

  const TradeTransaction({
    required this.idTransaksi,
    required this.idListing,
    required this.buyerUserId,
    required this.sellerUserId,
    required this.totalHarga,
    required this.metodeBayar,
    required this.status,
    this.txTransferHash,
    required this.tanggalTransaksi,
  });

  factory TradeTransaction.fromJson(Map<String, dynamic> json) {
    return TradeTransaction(
      idTransaksi: json['id_transaksi'] as int,
      idListing: json['id_listing'] as int,
      buyerUserId: json['buyer_user_id'] as int,
      sellerUserId: json['seller_user_id'] as int,
      totalHarga: (json['total_harga'] as num).toDouble(),
      metodeBayar: json['metode_bayar'] as String,
      status: json['status'] as String,
      txTransferHash: json['tx_transfer_hash'] as String?,
      tanggalTransaksi:
          DateTime.parse(json['tanggal_transaksi'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_transaksi': idTransaksi,
      'id_listing': idListing,
      'buyer_user_id': buyerUserId,
      'seller_user_id': sellerUserId,
      'total_harga': totalHarga,
      'metode_bayar': metodeBayar,
      'status': status,
      'tx_transfer_hash': txTransferHash,
      'tanggal_transaksi': tanggalTransaksi.toIso8601String(),
    };
  }
}
