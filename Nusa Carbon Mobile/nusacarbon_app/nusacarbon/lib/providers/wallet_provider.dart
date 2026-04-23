import 'package:flutter/material.dart';
import '../models/wallet_model.dart';
import '../models/blockchain_tx.dart';
import '../services/api_service.dart';

/// Loads the current user's wallet summary and their full blockchain
/// transaction history.
///
/// Wallet balance  → GET /api/wallet/{userId}
/// Tx history      → GET /api/blockchain/ledger?userId={userId}
///   (filtered server-side to entries where from_address or to_address
///    matches the user's wallet address)
class WalletProvider extends ChangeNotifier {
  WalletModel? _wallet;
  List<BlockchainTx> _transactions = [];
  bool _isLoading = false;
  String? _error;

  WalletModel? get wallet => _wallet;
  List<BlockchainTx> get transactions => _transactions;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Total tokens held — derived from the wallet summary returned by the API.
  double get totalBalance => (_wallet?.totalTokens ?? 0).toDouble();

  // ─── Load ──────────────────────────────────────────────────────────────

  Future<void> loadWallet(int userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final api = ApiService();

      // ── 1. Wallet summary ──────────────────────────────────────────────
      final walletRes = await api.getWallet(userId);
      if (walletRes.statusCode == 200) {
        final wData = walletRes.data['data'];
        if (wData != null) {
          _wallet = WalletModel.fromJson(wData as Map<String, dynamic>);
        }
      }

      // ── 2. Blockchain ledger entries for this user ─────────────────────
      // The backend filters by the user's wallet address (from_address OR
      // to_address) and returns entries in descending block-number order.
      final ledgerRes = await api.getBlockchainLedger(userId: userId);
      if (ledgerRes.statusCode == 200) {
        final raw = ledgerRes.data['data'] as List?;
        if (raw != null) {
          _transactions =
              raw
                  .map((e) => BlockchainTx.fromJson(e as Map<String, dynamic>))
                  .toList();
        }
      }
    } catch (e) {
      _error = e.toString();
      debugPrint('WalletProvider.loadWallet error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // ─── Refresh ───────────────────────────────────────────────────────────

  /// Re-fetches wallet + ledger. Called after a successful token purchase
  /// so the balance and history update immediately.
  Future<void> refresh(int userId) => loadWallet(userId);
}
