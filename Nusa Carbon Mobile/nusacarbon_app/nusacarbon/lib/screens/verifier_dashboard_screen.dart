import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../providers/verifier_provider.dart';
import '../providers/account_provider.dart';
import '../providers/auth_provider.dart';
import '../models/mrv_report.dart';
import '../widgets/status_badge.dart';
import '../widgets/review_bottom_sheet.dart';
import '../widgets/metric_card.dart';

class VerifierDashboardScreen extends StatefulWidget {
  const VerifierDashboardScreen({super.key});

  @override
  State<VerifierDashboardScreen> createState() => _VerifierDashboardScreenState();
}

class _VerifierDashboardScreenState extends State<VerifierDashboardScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      // AccountProvider.currentUserId returns 3 for the verifier role.
      final userId = context.read<AccountProvider>().currentUserId;
      context.read<VerifierProvider>().loadData(userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<VerifierProvider>();
    final account = context.watch<AccountProvider>();
    final auth = context.watch<AuthProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Verification Queue'),
        actions: [
            Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Chip(
                label: Text(
                  auth.user?.namaUser ?? 'Verifier',
                  style: const TextStyle(color: AppColors.indigo, fontSize: 12, fontWeight: FontWeight.bold),
                ),
                backgroundColor: AppColors.indigo.withValues(alpha: 0.1),
                side: BorderSide.none,
              ),
            ),
          ],
      ),
      body: provider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: () => provider.loadData(account.currentUserId),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  // ─── Metrics Grid ──────────────────────────────────
                  Row(
                    children: [
                      Expanded(child: MetricCardLight(label: 'Pending Review', value: provider.pendingCount.toString(), icon: Icons.pending_actions, iconColor: AppColors.pending)),
                      const SizedBox(width: 12),
                      Expanded(child: MetricCardLight(label: 'In Review', value: provider.inReviewCount.toString(), icon: Icons.preview, iconColor: AppColors.transfer)),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(child: MetricCardLight(label: 'Approved This Month', value: provider.approvedThisMonth.toString(), icon: Icons.verified, iconColor: AppColors.verified)),
                      const SizedBox(width: 12),
                      const Expanded(child: MetricCardLight(label: 'Avg MRV Score', value: '92%', icon: Icons.analytics, iconColor: AppColors.secondary)),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // ─── Task Queue ────────────────────────────────────
                  const Text('Task Queue', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                  const SizedBox(height: 12),
                  if (provider.queue.isEmpty)
                    const Center(child: Padding(padding: EdgeInsets.all(24), child: Text('No pending verifications.', style: TextStyle(color: AppColors.textMuted))))
                  else
                    ...provider.queue.map((mrv) => _TaskCard(
                      mrv: mrv,
                      onReview: () => _showReviewSheet(context, mrv, account.currentUserId),
                    )),

                  const SizedBox(height: 24),
                  // ─── Audit Log ─────────────────────────────────────
                  Theme(
                    data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
                    child: ExpansionTile(
                      title: const Text('Audit Log (Recent)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                      tilePadding: EdgeInsets.zero,
                      children: provider.auditLog.map((log) => ListTile(
                        contentPadding: EdgeInsets.zero,
                        leading: Icon(
                          log.hasil == 'approved' ? Icons.check_circle : Icons.warning,
                          color: log.hasil == 'approved' ? AppColors.verified : AppColors.pending,
                        ),
                        title: Text('Project ID: ${log.idMrv}', style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 14)),
                        subtitle: Text(log.verifiedAt.toString().substring(0, 10), style: const TextStyle(fontSize: 12)),
                        trailing: StatusBadge(status: log.hasil),
                      )).toList(),
                    ),
                  ),
                ],
              ),
            ),
    );
  }

  void _showReviewSheet(BuildContext context, MrvReport mrv, int verifierId) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => ReviewBottomSheet(
        mrvId: mrv.idMrv,
        verifierId: verifierId,
        projectName: mrv.namaProject ?? 'Project #${mrv.idProject}',
        // submitterName comes from the MRV report if available; falls back to
        // the project owner label so the sheet is never empty.
        developerName: mrv.submitterName ?? 'Project Owner',
        period: mrv.periodeMrv,
        estimatedCo2e: mrv.estimasiCo2e,
        onApprove: () => _showSnackbar(context, '✓ Report #${mrv.idMrv} Approved & token minting queued'),
        onReject: () => _showSnackbar(context, 'Report #${mrv.idMrv} Rejected', isError: true),
        onRequestChanges: () => _showSnackbar(context, 'Revision requested for Report #${mrv.idMrv}', isWarning: true),
      ),
    );
  }

  void _showSnackbar(BuildContext context, String message, {bool isError = false, bool isWarning = false}) {
    Color bg = AppColors.verified;
    if (isError) bg = AppColors.rejected;
    if (isWarning) bg = AppColors.pending;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: bg,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 3),
      ),
    );
  }
}

class _TaskCard extends StatelessWidget {
  final MrvReport mrv;
  final VoidCallback onReview;

  const _TaskCard({required this.mrv, required this.onReview});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    mrv.namaProject ?? 'Project ${mrv.idProject}',
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AppColors.textPrimary),
                    maxLines: 1, overflow: TextOverflow.ellipsis,
                  ),
                ),
                StatusBadge(status: mrv.statusMrv),
              ],
            ),
            const SizedBox(height: 4),
            Text('Developer: PT Hijau Nusantara', style: const TextStyle(fontSize: 13, color: AppColors.textSecondary)),
            const SizedBox(height: 12),
            Row(
              children: [
                const Icon(Icons.date_range, size: 14, color: AppColors.textMuted),
                const SizedBox(width: 4),
                Text('Submitted: ${mrv.createdAt.toString().substring(0, 10)}', style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                const Spacer(),
                const Text('Due in 3 days', style: TextStyle(fontSize: 12, color: AppColors.rejected, fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                const Icon(Icons.description, size: 14, color: AppColors.textMuted),
                const SizedBox(width: 4),
                const Text('3 Documents attached', style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
              ],
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: mrv.statusMrv == 'submitted'
                ? ElevatedButton(
                    onPressed: onReview,
                    style: ElevatedButton.styleFrom(backgroundColor: AppColors.indigo),
                    child: const Text('Start Review'),
                  )
                : OutlinedButton(
                    onPressed: onReview,
                    style: OutlinedButton.styleFrom(foregroundColor: AppColors.indigo, side: const BorderSide(color: AppColors.indigo)),
                    child: const Text('Continue Review'),
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
