import 'dart:convert';
import 'package:crypto/crypto.dart';

/// Blockchain simulation service using SHA-256 hashing.
///
/// No real blockchain integration — generates deterministic,
/// immutable-looking transaction hashes for the prototype.
class BlockchainService {
  BlockchainService._();

  /// Genesis hash — the "first block" in the chain
  static const String genesisHash =
      '0x0000000000000000000000000000000000000000000000000000000000000000';

  /// Generate a deterministic SHA-256 transaction hash.
  ///
  /// Input format: `previousHash|type|amount|refId|timestamp`
  /// Returns: `0x{sha256hex}`
  static String generateTxHash({
    required String previousHash,
    required String type, // mint | transfer | retire
    required double amount,
    required int refId,
    required String timestamp,
  }) {
    final input = '$previousHash|$type|$amount|$refId|$timestamp';
    final bytes = utf8.encode(input);
    final digest = sha256.convert(bytes);
    return '0x${digest.toString()}';
  }

  /// Truncate hash for display: `0x742d...8f3a`
  static String truncateHash(String hash) {
    if (hash.length < 12) return hash;
    return '${hash.substring(0, 6)}...${hash.substring(hash.length - 4)}';
  }

  /// Generate mock gas fee (0.003 – 0.007 ETH range)
  static double mockGasFee() {
    final fees = [0.003, 0.004, 0.005, 0.006, 0.007];
    return fees[DateTime.now().millisecond % fees.length];
  }

  /// Format gas fee for display
  static String formatGasFee(double fee) {
    return '~${fee.toStringAsFixed(3)} ETH';
  }
}
