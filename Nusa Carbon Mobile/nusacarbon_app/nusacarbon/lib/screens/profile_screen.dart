import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../providers/auth_provider.dart';
import '../providers/account_provider.dart';

import '../widgets/status_badge.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final account = context.watch<AccountProvider>();
    final user = auth.user;
    final role = auth.role;

    if (auth.isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (user == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // ─── Header ───────────────────────────────────────────
          Row(
            children: [
              CircleAvatar(
                radius: 32,
                backgroundColor: AppColors.primary.withValues(alpha: 0.1),
                child: const Icon(
                  Icons.person,
                  size: 32,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      user.namaUser,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      user.email,
                      style: const TextStyle(
                        fontSize: 14,
                        color: AppColors.textSecondary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        const Text(
                          'Verification Status: ',
                          style: TextStyle(
                            fontSize: 12,
                            color: AppColors.textMuted,
                          ),
                        ),
                        StatusBadge(status: user.statusKyc),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),

          // ─── KYC Checklist ────────────────────────────────────
          const Text(
            'KYC Checklist',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 8),
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.border),
            ),
            child: Column(
              children: [
                _KycItem(
                  label: 'Identity Verification',
                  isComplete: user.statusKyc == 'verified',
                  onTap: () {},
                ),
                const Divider(),
                _KycItem(
                  label: 'Business Documentation',
                  isComplete: user.statusKyc == 'verified',
                  onTap: () {},
                ),
                const Divider(),
                _KycItem(
                  label: 'Bank Account',
                  isComplete: user.statusKyc == 'verified',
                  onTap: () {},
                ),
                const Divider(),
                _KycItem(
                  label: 'Wallet Connection',
                  isComplete: user.statusKyc != 'unverified',
                  onTap: () {},
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // ─── Dual Role Toggle (Mock) ──────────────────────────
          if (role == 'buyer' || role == 'project_owner') ...[
            const Text(
              'Account Mode',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: AppColors.textPrimary,
              ),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: AppColors.primary.withValues(alpha: 0.3),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    account.isDeveloper
                        ? Icons.business_center
                        : Icons.person_outline,
                    color: AppColors.primary,
                  ),
                  const SizedBox(width: 12),
                  Text(
                    account.isDeveloper
                        ? 'Project Developer Mode'
                        : 'Investor Mode',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: AppColors.primary,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
          ],

          // ─── Organization Details ─────────────────────────────
          const Text(
            'Organization Details',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.border),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _OrgDetail(label: 'Company Name', value: user.namaUser),
                _OrgDetail(label: 'Business Type', value: _businessType(role)),
                _OrgDetail(
                  label: 'Registration Number',
                  value: 'ID-2024-#${user.idUser.toString().padLeft(6, '0')}',
                ),
                _OrgDetail(label: 'Location', value: 'Jakarta, Indonesia'),
                _OrgDetail(
                  label: 'Member Since',
                  value:
                      '${_monthName(user.createdAt.month)} ${user.createdAt.year}',
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: () {},
                    child: const Text('Edit Organization Info'),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // ─── Linked Wallet ────────────────────────────────────
          const Text(
            'Linked Blockchain Wallet',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.border),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(6),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF6851B).withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Icon(
                        Icons.account_balance_wallet,
                        color: Color(0xFFF6851B),
                        size: 18,
                      ),
                    ),
                    const SizedBox(width: 8),
                    const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'MetaMask',
                          style: TextStyle(fontWeight: FontWeight.w600),
                        ),
                        Text(
                          'Ethereum Mainnet',
                          style: TextStyle(
                            fontSize: 12,
                            color: AppColors.textMuted,
                          ),
                        ),
                      ],
                    ),
                    const Spacer(),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.verifiedBg,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        children: const [
                          Icon(
                            Icons.circle,
                            size: 8,
                            color: AppColors.verified,
                          ),
                          SizedBox(width: 4),
                          Text(
                            'Active',
                            style: TextStyle(
                              fontSize: 10,
                              color: AppColors.verified,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                const Text(
                  '0x742d355Cc6634C853925a3b944fc9ef13a',
                  style: TextStyle(
                    fontFamily: 'monospace',
                    fontSize: 13,
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: () {},
                    child: const Text('Change Wallet'),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // ─── Dashboard Links ──────────────────────────────────
          if (role == 'project_owner')
            _DashboardLink(
              title: 'Manage Projects',
              icon: Icons.dashboard,
              color: AppColors.secondary,
              onTap: () => context.go('/dashboard/owner'),
            ),
          if (role == 'verifier')
            _DashboardLink(
              title: 'Verification Queue',
              icon: Icons.fact_check,
              color: AppColors.indigo,
              onTap: () => context.go('/dashboard/verifier'),
            ),
          if (role == 'admin')
            _DashboardLink(
              title: 'Admin Panel',
              icon: Icons.admin_panel_settings,
              color: AppColors.dark,
              onTap: () => context.go('/admin'),
            ),

          if (role != 'buyer') const SizedBox(height: 24),

          // ─── Settings ─────────────────────────────────────────
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.border),
            ),
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.notifications_outlined),
                  title: const Text('Notifications'),
                  trailing: Badge(
                    label: const Text('2'),
                    child: const Icon(Icons.chevron_right),
                  ),
                  onTap: () {},
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.lock_outline),
                  title: const Text('Security & Privacy'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {},
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.help_outline),
                  title: const Text('Help & Support'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {},
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // ─── Logout ───────────────────────────────────────────
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: () {
                auth.logout(accountProvider: account);
                context.go('/splash');
              },
              icon: const Icon(Icons.logout, color: AppColors.rejected),
              label: const Text(
                'Log Out',
                style: TextStyle(color: AppColors.rejected),
              ),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: AppColors.rejected),
              ),
            ),
          ),
          const SizedBox(height: 24),

          // ─── Version ──────────────────────────────────────────
          const Center(
            child: Text(
              'NusaCarbon v1.0.0',
              style: TextStyle(fontSize: 12, color: AppColors.textMuted),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }
}

// ─── Private helpers ──────────────────────────────────────────────────────────

String _businessType(String? role) {
  switch (role) {
    case 'project_owner':
      return 'Carbon Project Developer';
    case 'verifier':
      return 'Independent Auditor';
    case 'admin':
      return 'Platform Administrator';
    default:
      return 'Carbon Token Investor';
  }
}

String _monthName(int month) {
  const months = [
    '',
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];
  return months[month];
}

class _KycItem extends StatelessWidget {
  final String label;
  final bool isComplete;
  final VoidCallback onTap;
  const _KycItem({
    required this.label,
    required this.isComplete,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(
        isComplete ? Icons.check_circle : Icons.radio_button_unchecked,
        color: isComplete ? AppColors.verified : AppColors.textMuted,
      ),
      title: Text(label, style: const TextStyle(fontSize: 14)),
      trailing: const Icon(Icons.chevron_right, size: 20),
      onTap: onTap,
    );
  }
}

class _OrgDetail extends StatelessWidget {
  final String label;
  final String value;
  const _OrgDetail({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 2,
            child: Text(
              label,
              style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
            ),
          ),
          Expanded(
            flex: 3,
            child: Text(
              value,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w500,
                color: AppColors.textPrimary,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _DashboardLink extends StatelessWidget {
  final String title;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;
  const _DashboardLink({
    required this.title,
    required this.icon,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 24),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: ListTile(
        leading: Icon(icon, color: color),
        title: Text(
          title,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: color,
          ),
        ),
        trailing: Icon(Icons.arrow_forward, color: color),
        onTap: onTap,
      ),
    );
  }
}
