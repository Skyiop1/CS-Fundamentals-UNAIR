import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../providers/wallet_provider.dart';
import '../services/api_service.dart';
import '../services/blockchain_service.dart';

/// Sticky bottom-bar widget on ProjectDetailScreen that lets an Investor
/// buy tokens from a specific marketplace listing.
///
/// Calls POST /api/transactions/buy with the real listing ID and buyer user ID,
/// then refreshes WalletProvider so the balance updates immediately.
class BuyTokenWidget extends StatefulWidget {
  /// The marketplace listing being purchased from.
  final int idListing;

  /// The authenticated buyer's database user ID.
  final int buyerUserId;

  final String projectName;
  final int vintageYear;
  final double pricePerToken;

  /// Maximum tokens available in this listing (prevents over-ordering).
  final int maxAvailable;

  /// Optional callback invoked after a successful purchase.
  final VoidCallback? onPurchaseComplete;

  const BuyTokenWidget({
    super.key,
    required this.idListing,
    required this.buyerUserId,
    required this.projectName,
    required this.vintageYear,
    required this.pricePerToken,
    this.maxAvailable = 9999,
    this.onPurchaseComplete,
  });

  @override
  State<BuyTokenWidget> createState() => _BuyTokenWidgetState();
}

class _BuyTokenWidgetState extends State<BuyTokenWidget> {
  int _quantity = 1;
  bool _isBuying = false;
  final _controller = TextEditingController(text: '1');

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  double get _total => _quantity * widget.pricePerToken;

  // ─── API call ─────────────────────────────────────────────────────────

  Future<void> _executeBuy() async {
    if (_isBuying) return;

    setState(() => _isBuying = true);

    try {
      final api = ApiService();
      final body = {
        'id_listing': widget.idListing,
        'buyer_user_id': widget.buyerUserId,
        'jumlah': _quantity,
        'metode_bayar': 'wallet',
      };

      final res = await api.buyTokens(body);

      if (!mounted) return;

      if (res.statusCode == 201 || res.statusCode == 200) {
        final data = res.data['data'] as Map<String, dynamic>?;

        // Refresh wallet balance + history in the background
        context.read<WalletProvider>().refresh(widget.buyerUserId);

        widget.onPurchaseComplete?.call();
        _showSuccessSheet(context, data);
      } else {
        final msg = res.data['message'] as String? ?? 'Purchase failed.';
        _showError(msg);
      }
    } catch (e) {
      if (!mounted) return;
      _showError('Could not connect to server. Please try again.');
      debugPrint('BuyTokenWidget._executeBuy error: $e');
    } finally {
      if (mounted) setState(() => _isBuying = false);
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: AppColors.rejected,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  // ─── Build ────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final idr = NumberFormat.currency(
      locale: 'id_ID',
      symbol: 'Rp ',
      decimalDigits: 0,
    );
    final fmt = NumberFormat('#,###');

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 16,
            offset: const Offset(0, -4),
          ),
        ],
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // ─── Price + Quantity row ─────────────────────────────────
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Vintage ${widget.vintageYear}',
                      style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.textMuted,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '${idr.format(widget.pricePerToken)} per tCO₂e',
                      style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                        color: AppColors.textPrimary,
                      ),
                    ),
                  ],
                ),
                Row(
                  children: [
                    _QtyBtn(
                      icon: Icons.remove,
                      onTap:
                          _isBuying
                              ? null
                              : () {
                                if (_quantity > 1) {
                                  setState(() {
                                    _quantity--;
                                    _controller.text = '$_quantity';
                                  });
                                }
                              },
                    ),
                    SizedBox(
                      width: 50,
                      child: TextField(
                        controller: _controller,
                        textAlign: TextAlign.center,
                        keyboardType: TextInputType.number,
                        enabled: !_isBuying,
                        decoration: const InputDecoration(
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.zero,
                        ),
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                        ),
                        onChanged: (v) {
                          final n = int.tryParse(v);
                          if (n != null && n > 0) {
                            setState(() {
                              _quantity = n.clamp(1, widget.maxAvailable);
                            });
                          }
                        },
                      ),
                    ),
                    _QtyBtn(
                      icon: Icons.add,
                      onTap:
                          _isBuying
                              ? null
                              : () {
                                if (_quantity < widget.maxAvailable) {
                                  setState(() {
                                    _quantity++;
                                    _controller.text = '$_quantity';
                                  });
                                }
                              },
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 12),

            // ─── Total summary ────────────────────────────────────────
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.verifiedBg,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '${fmt.format(_quantity)} tokens × ${idr.format(widget.pricePerToken)}',
                    style: const TextStyle(
                      fontSize: 13,
                      color: AppColors.textSecondary,
                    ),
                  ),
                  Text(
                    idr.format(_total),
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: AppColors.primary,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 4),
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                '= ${fmt.format(_quantity)} tCO₂e offset',
                style: const TextStyle(
                  fontSize: 12,
                  color: AppColors.textMuted,
                ),
              ),
            ),
            const SizedBox(height: 12),

            // ─── Buy button ───────────────────────────────────────────
            SizedBox(
              width: double.infinity,
              child:
                  _isBuying
                      ? Container(
                        height: 48,
                        decoration: BoxDecoration(
                          gradient: AppColors.primaryGradient,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Center(
                          child: SizedBox(
                            width: 22,
                            height: 22,
                            child: CircularProgressIndicator(
                              strokeWidth: 2.5,
                              valueColor: AlwaysStoppedAnimation(Colors.white),
                            ),
                          ),
                        ),
                      )
                      : DecoratedBox(
                        decoration: BoxDecoration(
                          gradient: AppColors.primaryGradient,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: ElevatedButton(
                          onPressed: _executeBuy,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.transparent,
                            shadowColor: Colors.transparent,
                            foregroundColor: Colors.white,
                            minimumSize: const Size(double.infinity, 48),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          child: const Text(
                            'Buy Tokens',
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                      ),
            ),
          ],
        ),
      ),
    );
  }

  // ─── Success bottom sheet ─────────────────────────────────────────────

  void _showSuccessSheet(BuildContext context, Map<String, dynamic>? data) {
    final idr = NumberFormat.currency(
      locale: 'id_ID',
      symbol: 'Rp ',
      decimalDigits: 0,
    );
    final fmt = NumberFormat('#,###');

    // Use the real tx hash from the API response; fall back to a generated one
    // only when the server doesn't return one (should not happen in production).
    final rawHash =
        data?['tx_transfer_hash'] as String? ??
        data?['tx_hash'] as String? ??
        BlockchainService.generateTxHash(
          previousHash: BlockchainService.genesisHash,
          type: 'transfer',
          amount: _quantity.toDouble(),
          refId: DateTime.now().millisecond,
          timestamp: DateTime.now().toIso8601String(),
        );

    final tokensBought = (data?['token_count'] as num?)?.toInt() ?? _quantity;
    final totalPaid = (data?['total_harga'] as num?)?.toDouble() ?? _total;
    final namaProject = data?['nama_project'] as String? ?? widget.projectName;
    final txId = data?['id_transaksi'] as int?;

    showModalBottomSheet(
      context: context,
      isDismissible: false,
      backgroundColor: Colors.transparent,
      builder:
          (_) => Container(
            padding: const EdgeInsets.all(24),
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Handle
                Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: AppColors.border,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
                const SizedBox(height: 20),

                // Success icon
                Container(
                  width: 72,
                  height: 72,
                  decoration: BoxDecoration(
                    color: AppColors.verifiedBg,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.check_circle,
                    color: AppColors.verified,
                    size: 44,
                  ),
                ),
                const SizedBox(height: 16),

                const Text(
                  'Purchase Successful!',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'You purchased ${fmt.format(tokensBought)} tCO₂e from $namaProject',
                  style: const TextStyle(
                    fontSize: 14,
                    color: AppColors.textSecondary,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),

                // Transaction detail card
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppColors.background,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: AppColors.border),
                  ),
                  child: Column(
                    children: [
                      _DetailRow('Total Paid', idr.format(totalPaid)),
                      const SizedBox(height: 8),
                      _DetailRow('Tokens', '${fmt.format(tokensBought)} tCO₂e'),
                      if (txId != null) ...[
                        const SizedBox(height: 8),
                        _DetailRow('Tx ID', '#$txId'),
                      ],
                      const SizedBox(height: 8),
                      _DetailRow(
                        'Tx Hash',
                        BlockchainService.truncateHash(rawHash),
                        mono: true,
                      ),
                      const SizedBox(height: 8),
                      _DetailRow('Status', 'Confirmed ✓'),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('Done'),
                  ),
                ),
                const SizedBox(height: 8),
              ],
            ),
          ),
    );
  }
}

// ─── Sub-widgets ────────────────────────────────────────────────────────────

class _QtyBtn extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onTap;

  const _QtyBtn({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final enabled = onTap != null;
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(6),
        decoration: BoxDecoration(
          border: Border.all(
            color:
                enabled
                    ? AppColors.border
                    : AppColors.border.withValues(alpha: 0.4),
          ),
          borderRadius: BorderRadius.circular(6),
        ),
        child: Icon(
          icon,
          size: 16,
          color: enabled ? AppColors.textPrimary : AppColors.textMuted,
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final String label;
  final String value;
  final bool mono;

  const _DetailRow(this.label, this.value, {this.mono = false});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: AppColors.textMuted),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
            fontFamily: mono ? 'monospace' : null,
          ),
        ),
      ],
    );
  }
}
