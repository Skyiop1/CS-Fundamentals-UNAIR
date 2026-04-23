import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../constants/app_colors.dart';
import '../models/blockchain_tx.dart';
import '../services/blockchain_service.dart';

/// Blockchain transaction tile for Wallet and Ledger views.
///
/// Shows: type icon, type label, status, amount, project name,
/// timestamp, truncated hash, gas fee
class BlockchainTxTile extends StatelessWidget {
  final BlockchainTx tx;
  final VoidCallback? onTap;

  const BlockchainTxTile({
    super.key,
    required this.tx,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final formatter = NumberFormat('#,###');
    final config = _getTxConfig(tx.type);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(12),
        margin: const EdgeInsets.only(bottom: 8),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.border, width: 0.5),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ─── Row 1: Type + Status + Amount ──────────
            Row(
              children: [
                // Type icon
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: config.bgColor,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(config.icon, color: config.color, size: 18),
                ),
                const SizedBox(width: 10),
                // Type label + status
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        config.label,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Row(
                        children: [
                          Icon(
                            tx.status == 'confirmed'
                                ? Icons.check_circle
                                : Icons.hourglass_empty,
                            size: 12,
                            color: tx.status == 'confirmed'
                                ? AppColors.verified
                                : AppColors.pending,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            tx.status == 'confirmed'
                                ? 'Confirmed'
                                : 'Pending',
                            style: TextStyle(
                              fontSize: 11,
                              color: tx.status == 'confirmed'
                                  ? AppColors.verified
                                  : AppColors.pending,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                // Amount
                Text(
                  '${config.sign}${formatter.format(tx.amount.toInt())} tCO₂e',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: config.color,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),

            // ─── Row 2: Project name + timestamp ────────
            if (tx.projectName != null)
              Text(
                tx.projectName!,
                style: const TextStyle(
                  fontSize: 12,
                  color: AppColors.textSecondary,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            const SizedBox(height: 4),

            // ─── Row 3: Hash + Gas Fee ──────────────────
            Row(
              children: [
                Text(
                  BlockchainService.truncateHash(tx.hash),
                  style: const TextStyle(
                    fontFamily: 'monospace',
                    fontSize: 11,
                    color: AppColors.textMuted,
                    letterSpacing: 0.5,
                  ),
                ),
                const Spacer(),
                Text(
                  'Gas Fee: ${BlockchainService.formatGasFee(tx.gasFeeMock)}',
                  style: const TextStyle(
                    fontSize: 10,
                    color: AppColors.textMuted,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  _TxConfig _getTxConfig(String type) {
    switch (type) {
      case 'mint':
        return _TxConfig(
          label: 'Mint',
          icon: Icons.add_circle_outline,
          color: AppColors.verified,
          bgColor: AppColors.verifiedBg,
          sign: '+',
        );
      case 'transfer':
        return _TxConfig(
          label: 'Transfer',
          icon: Icons.swap_horiz,
          color: AppColors.transfer,
          bgColor: AppColors.transferBg,
          sign: '-',
        );
      case 'retire':
        return _TxConfig(
          label: 'Retire',
          icon: Icons.local_fire_department,
          color: AppColors.rejected,
          bgColor: AppColors.rejectedBg,
          sign: '-',
        );
      default:
        return _TxConfig(
          label: type,
          icon: Icons.info_outline,
          color: AppColors.textSecondary,
          bgColor: AppColors.border,
          sign: '',
        );
    }
  }
}

class _TxConfig {
  final String label;
  final IconData icon;
  final Color color;
  final Color bgColor;
  final String sign;

  const _TxConfig({
    required this.label,
    required this.icon,
    required this.color,
    required this.bgColor,
    required this.sign,
  });
}
