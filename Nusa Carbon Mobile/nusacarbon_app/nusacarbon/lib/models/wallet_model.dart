class WalletModel {
  final int idWallet;
  final int idUser;
  final String walletAddress; // "0x742d355Cc6634C853925a3b944fc9ef13a"
  final String chainNetwork; // "ethereum" (mock)
  final int totalTokens;
  final int availableTokens;
  final int listedTokens;
  final int soldTokens;
  final int retiredTokens;
  final double idrBalance;
  final DateTime createdAt;

  const WalletModel({
    required this.idWallet,
    required this.idUser,
    required this.walletAddress,
    required this.chainNetwork,
    this.totalTokens = 0,
    this.availableTokens = 0,
    this.listedTokens = 0,
    this.soldTokens = 0,
    this.retiredTokens = 0,
    this.idrBalance = 0.0,
    required this.createdAt,
  });

  factory WalletModel.fromJson(Map<String, dynamic> json) {
    return WalletModel(
      idWallet: (json['id_wallet'] as num?)?.toInt() ?? 0,
      idUser: (json['id_user'] as num?)?.toInt() ?? 0,
      walletAddress: json['wallet_address']?.toString() ?? '',
      chainNetwork: json['chain_network']?.toString() ?? 'ethereum',
      totalTokens: (json['total_tokens'] as num?)?.toInt() ?? 0,
      availableTokens: (json['available_tokens'] as num?)?.toInt() ?? 0,
      listedTokens: (json['listed_tokens'] as num?)?.toInt() ?? 0,
      soldTokens: (json['sold_tokens'] as num?)?.toInt() ?? 0,
      retiredTokens: (json['retired_tokens'] as num?)?.toInt() ?? 0,
      idrBalance: (json['idr_balance'] as num?)?.toDouble() ?? 0.0,
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_wallet': idWallet,
      'id_user': idUser,
      'wallet_address': walletAddress,
      'chain_network': chainNetwork,
      'total_tokens': totalTokens,
      'available_tokens': availableTokens,
      'listed_tokens': listedTokens,
      'sold_tokens': soldTokens,
      'retired_tokens': retiredTokens,
      'idrBalance': idrBalance,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
