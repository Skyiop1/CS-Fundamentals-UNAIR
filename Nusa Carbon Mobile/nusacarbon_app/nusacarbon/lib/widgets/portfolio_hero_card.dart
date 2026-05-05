import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../constants/app_colors.dart';

/// Portfolio hero card with emerald gradient.
///
/// Shows: total portfolio value (IDR), percentage change,
/// total carbon tokens held (tCO₂e)
class PortfolioHeroCard extends StatelessWidget {
  final double portfolioValue;
  final double totalTokens;
  final double monthlyChange;
  final VoidCallback? onPortfolioTap;

  const PortfolioHeroCard({
    super.key,
    required this.portfolioValue,
    required this.totalTokens,
    required this.monthlyChange,
    this.onPortfolioTap,
  });

  @override
  Widget build(BuildContext context) {
    final idrFormatter = NumberFormat.currency(
      locale: 'id_ID',
      symbol: 'Rp ',
      decimalDigits: 0,
    );

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: AppColors.primaryGradient,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.3),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Label
          Text(
            'Saldo Rupiah',
            style: TextStyle(
              fontSize: 14,
              color: Colors.white.withValues(alpha: 0.85),
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 4),

          // Portfolio value (IDR)
          Text(
            idrFormatter.format(portfolioValue),
            style: const TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.bold,
              color: Colors.white,
              letterSpacing: -0.5,
            ),
          ),
          const SizedBox(height: 16),

          // Divider
          Container(
            height: 1,
            color: Colors.white.withValues(alpha: 0.2),
          ),
          const SizedBox(height: 16),

          // Quick actions (Deposit/Withdraw) inside the card
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _HeroAction(
                icon: Icons.add_circle,
                label: 'Top Up',
                onTap: onPortfolioTap,
              ),
              Container(
                width: 1,
                height: 30,
                color: Colors.white.withValues(alpha: 0.2),
              ),
              _HeroAction(
                icon: Icons.arrow_circle_up,
                label: 'Withdraw',
                onTap: onPortfolioTap,
              ),
              Container(
                width: 1,
                height: 30,
                color: Colors.white.withValues(alpha: 0.2),
              ),
              _HeroAction(
                icon: Icons.history,
                label: 'History',
                onTap: onPortfolioTap,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _HeroAction extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback? onTap;

  const _HeroAction({
    required this.icon,
    required this.label,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: Colors.white, size: 20),
          const SizedBox(width: 6),
          Text(
            label,
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w600,
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }
}
