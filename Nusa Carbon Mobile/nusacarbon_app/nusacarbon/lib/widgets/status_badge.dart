import 'package:flutter/material.dart';
import '../constants/app_colors.dart';

/// Reusable status badge chip with icon and color coding.
///
/// Supports: verified, pending, rejected, active, retired,
/// draft, submitted, under_review, available, listed, sold
class StatusBadge extends StatelessWidget {
  final String status;
  final double fontSize;

  const StatusBadge({
    super.key,
    required this.status,
    this.fontSize = 12,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getConfig(status.toLowerCase());

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: config.bgColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(config.icon, color: config.textColor, size: fontSize + 2),
          const SizedBox(width: 4),
          Text(
            config.label,
            style: TextStyle(
              color: config.textColor,
              fontSize: fontSize,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  _BadgeConfig _getConfig(String status) {
    switch (status) {
      case 'verified':
      case 'active':
      case 'available':
      case 'approved':
      case 'completed':
      case 'confirmed':
      case 'success':
        return _BadgeConfig(
          label: _capitalizeFirst(status),
          icon: Icons.check_circle,
          textColor: AppColors.verified,
          bgColor: AppColors.verifiedBg,
        );
      case 'pending':
      case 'submitted':
      case 'under_review':
      case 'listed':
      case 'revision_needed':
        return _BadgeConfig(
          label: status == 'under_review'
              ? 'Under Review'
              : status == 'revision_needed'
                  ? 'Revision Needed'
                  : _capitalizeFirst(status),
          icon: Icons.hourglass_empty,
          textColor: AppColors.pending,
          bgColor: AppColors.pendingBg,
        );
      case 'rejected':
      case 'failed':
      case 'retired':
        return _BadgeConfig(
          label: _capitalizeFirst(status),
          icon: status == 'retired'
              ? Icons.local_fire_department
              : Icons.cancel,
          textColor: AppColors.rejected,
          bgColor: AppColors.rejectedBg,
        );
      case 'draft':
        return _BadgeConfig(
          label: 'Draft',
          icon: Icons.edit_note,
          textColor: AppColors.textMuted,
          bgColor: AppColors.border,
        );
      case 'sold':
        return _BadgeConfig(
          label: 'Sold',
          icon: Icons.swap_horiz,
          textColor: AppColors.transfer,
          bgColor: AppColors.transferBg,
        );
      default:
        return _BadgeConfig(
          label: _capitalizeFirst(status),
          icon: Icons.info_outline,
          textColor: AppColors.textSecondary,
          bgColor: AppColors.border,
        );
    }
  }

  String _capitalizeFirst(String s) {
    if (s.isEmpty) return s;
    return s[0].toUpperCase() + s.substring(1);
  }
}

class _BadgeConfig {
  final String label;
  final IconData icon;
  final Color textColor;
  final Color bgColor;

  const _BadgeConfig({
    required this.label,
    required this.icon,
    required this.textColor,
    required this.bgColor,
  });
}
