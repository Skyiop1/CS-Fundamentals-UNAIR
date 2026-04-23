import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:intl/intl.dart';
import '../constants/app_colors.dart';
import '../models/carbon_token.dart';
import '../services/blockchain_service.dart';
import 'status_badge.dart';

/// Full token card widget as specified in system instructions.
///
/// Shows: project image, status badge, verification badge,
/// project name, location, amount tCO₂e, vintage year, token ID
class TokenCard extends StatelessWidget {
  final CarbonToken token;
  final VoidCallback? onTap;

  const TokenCard({
    super.key,
    required this.token,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final formatter = NumberFormat('#,###');

    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.06),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ─── Image with badge overlay ──────────────────────
            Stack(
              children: [
                ClipRRect(
                  borderRadius:
                      const BorderRadius.vertical(top: Radius.circular(12)),
                  child: CachedNetworkImage(
                    imageUrl: token.imageUrl ?? '',
                    height: 120,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    placeholder: (_, __) => Container(
                      height: 120,
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          colors: [Color(0xFFD1FAE5), Color(0xFFCCFBF1)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                      child: const Center(
                        child: Icon(Icons.eco, color: AppColors.primary, size: 40),
                      ),
                    ),
                    errorWidget: (_, __, ___) => Container(
                      height: 120,
                      color: const Color(0xFFECFDF5),
                      child: const Center(
                        child: Icon(Icons.eco, color: AppColors.primary, size: 40),
                      ),
                    ),
                  ),
                ),
                // Status badge overlay
                Positioned(
                  top: 8,
                  left: 8,
                  child: StatusBadge(status: token.statusToken),
                ),
                // Verification standard badge
                Positioned(
                  top: 8,
                  right: 8,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.9),
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(
                        color: AppColors.border,
                        width: 0.5,
                      ),
                    ),
                    child: Text(
                      _getVerificationStandard(token.namaKategori),
                      style: const TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w600,
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ),
                ),
              ],
            ),

            // ─── Content ──────────────────────────────────────
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Project name
                  Text(
                    token.namaProject,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),

                  // Location
                  Row(
                    children: [
                      const Icon(
                        Icons.location_on,
                        size: 14,
                        color: AppColors.textMuted,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        token.lokasi,
                        style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textMuted,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),

                  // Amount · Vintage · Token ID
                  Row(
                    children: [
                      // Amount
                      _InfoChip(
                        label:
                            '${formatter.format(token.amount ?? 0)} tCO₂e',
                        icon: Icons.eco,
                      ),
                      const SizedBox(width: 8),
                      // Vintage
                      _InfoChip(
                        label: '${token.vintageYear}',
                        icon: Icons.calendar_today,
                      ),
                      const Spacer(),
                      // Token ID (truncated hash)
                      if (token.txMintHash != null)
                        Text(
                          BlockchainService.truncateHash(token.txMintHash!),
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 11,
                            color: AppColors.textMuted,
                            letterSpacing: 0.5,
                          ),
                        ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getVerificationStandard(String category) {
    if (category.toLowerCase().contains('hutan') ||
        category.toLowerCase().contains('forest')) {
      return 'GOLD STANDARD';
    }
    return 'VERRA VCS';
  }
}

class _InfoChip extends StatelessWidget {
  final String label;
  final IconData icon;

  const _InfoChip({required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 12, color: AppColors.textMuted),
        const SizedBox(width: 3),
        Text(
          label,
          style: const TextStyle(
            fontSize: 11,
            color: AppColors.textSecondary,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }
}
