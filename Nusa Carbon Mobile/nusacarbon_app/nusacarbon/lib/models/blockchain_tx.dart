class BlockchainTx {
  final String hash; // Full SHA-256 hash
  final String previousHash; // Chain linking
  final String timestamp;
  final String type; // mint | transfer | retire
  final double amount; // tCO₂e
  final String? fromAddress;
  final String? toAddress;
  final int blockNumber;
  final double gasFeeMock; // e.g., 0.004 (ETH, for display only)
  // Derived fields for display
  final String? projectName;
  final String? status; // confirmed | pending

  const BlockchainTx({
    required this.hash,
    required this.previousHash,
    required this.timestamp,
    required this.type,
    required this.amount,
    this.fromAddress,
    this.toAddress,
    required this.blockNumber,
    required this.gasFeeMock,
    this.projectName,
    this.status,
  });

  factory BlockchainTx.fromJson(Map<String, dynamic> json) {
    return BlockchainTx(
      hash: (json['tx_hash'] ?? json['hash'] ?? '').toString(),
      previousHash: (json['prev_hash'] ?? json['previous_hash'] ?? '').toString(),
      timestamp: (json['created_at'] ?? json['timestamp'] ?? '').toString(),
      type: (json['tx_type'] ?? json['type'] ?? 'transfer').toString(),
      amount: ((json['amount_co2e'] ?? json['amount'] ?? 0) as num).toDouble(),
      fromAddress: json['from_address']?.toString(),
      toAddress: json['to_address']?.toString(),
      blockNumber: (json['block_number'] as num?)?.toInt() ?? 0,
      gasFeeMock: (json['gas_fee_mock'] as num?)?.toDouble() ?? 0.004,
      projectName: json['project_name']?.toString(),
      status: json['status']?.toString() ?? 'confirmed',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'hash': hash,
      'previous_hash': previousHash,
      'timestamp': timestamp,
      'type': type,
      'amount': amount,
      'from_address': fromAddress,
      'to_address': toAddress,
      'block_number': blockNumber,
      'gas_fee_mock': gasFeeMock,
      'project_name': projectName,
      'status': status,
    };
  }
}
