import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../constants/app_colors.dart';
import '../providers/owner_provider.dart';
import '../providers/account_provider.dart';
import '../models/carbon_project.dart';
import '../widgets/status_badge.dart';
import '../widgets/metric_card.dart';
import '../widgets/mrv_upload_sheet.dart';

class OwnerDashboardScreen extends StatefulWidget {
  const OwnerDashboardScreen({super.key});

  @override
  State<OwnerDashboardScreen> createState() => _OwnerDashboardScreenState();
}

class _OwnerDashboardScreenState extends State<OwnerDashboardScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final userId = context.read<AccountProvider>().currentUserId;
      context.read<OwnerProvider>().loadData(userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<OwnerProvider>();
    final account = context.watch<AccountProvider>();
    final idr = NumberFormat.currency(locale: 'id_ID', symbol: 'Rp ', decimalDigits: 0);
    final fmt = NumberFormat('#,###');

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Projects'),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Chip(
              label: const Text('Owner', style: TextStyle(color: AppColors.secondary, fontSize: 12, fontWeight: FontWeight.bold)),
              backgroundColor: AppColors.secondary.withValues(alpha: 0.1),
              side: BorderSide.none,
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showSubmitProjectSheet(context),
        icon: const Icon(Icons.add),
        label: const Text('Submit Project'),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
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
                      Expanded(child: MetricCardLight(label: 'Total Minted', value: fmt.format(provider.totalMinted), icon: Icons.eco, iconColor: AppColors.primary)),
                      const SizedBox(width: 12),
                      Expanded(child: MetricCardLight(label: 'Tokens Sold', value: fmt.format(provider.tokensSold), icon: Icons.shopping_cart, iconColor: AppColors.secondary)),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(child: MetricCardLight(label: 'Total Revenue', value: idr.format(provider.totalRevenue), icon: Icons.account_balance_wallet, iconColor: AppColors.transfer)),
                      const SizedBox(width: 12),
                      Expanded(child: MetricCardLight(label: 'Active Projects', value: provider.activeCount.toString(), icon: Icons.domain_verification, iconColor: AppColors.verified)),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // ─── Project List ──────────────────────────────────
                  const Text('Project Portfolio', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                  const SizedBox(height: 12),
                  if (provider.projects.isEmpty)
                    const Center(child: Padding(padding: EdgeInsets.all(24), child: Text('No projects found.', style: TextStyle(color: AppColors.textMuted))))
                  else
                    ...provider.projects.map((p) => _OwnerProjectCard(
                      project: p, 
                      onUpdateMrv: () => _showMrvUploadSheet(context),
                      onViewInMarket: () => context.go('/project/${p.idProject}'),
                    )),
                  
                  const SizedBox(height: 80), // Space for FAB
                ],
              ),
            ),
    );
  }

  void _showMrvUploadSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => const MrvUploadSheet(),
    );
  }

  void _showSubmitProjectSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.9, maxChildSize: 0.95, minChildSize: 0.5,
        builder: (_, scrollController) => Container(
          padding: const EdgeInsets.all(20),
          decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
          child: ListView(
            controller: scrollController,
            children: [
              Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),
              const SizedBox(height: 16),
              const Text('Submit New Project', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 20),
              TextField(decoration: const InputDecoration(labelText: 'Project Name')),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                items: ['Hutan', 'Mangrove', 'Energi Terbarukan', 'Blue Carbon', 'Lahan Gambut'].map((c) => DropdownMenuItem(value: c, child: Text(c))).toList(),
                onChanged: (_) {},
                decoration: const InputDecoration(labelText: 'Category'),
              ),
              const SizedBox(height: 12),
              TextField(decoration: const InputDecoration(labelText: 'Location Name')),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(child: TextField(decoration: const InputDecoration(labelText: 'Latitude'), keyboardType: TextInputType.number)),
                  const SizedBox(width: 12),
                  Expanded(child: TextField(decoration: const InputDecoration(labelText: 'Longitude'), keyboardType: TextInputType.number)),
                ],
              ),
              const SizedBox(height: 12),
              TextField(decoration: const InputDecoration(labelText: 'Land Area (Hectares)'), keyboardType: TextInputType.number),
              const SizedBox(height: 12),
              TextField(decoration: const InputDecoration(labelText: 'Description'), maxLines: 3),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () { 
                  Navigator.pop(context); 
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Project submitted for review')));
                }, 
                child: const Text('Submit Project')
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _OwnerProjectCard extends StatelessWidget {
  final CarbonProject project;
  final VoidCallback onUpdateMrv;
  final VoidCallback onViewInMarket;

  const _OwnerProjectCard({required this.project, required this.onUpdateMrv, required this.onViewInMarket});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        project.namaProject,
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textPrimary),
                        maxLines: 1, overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    StatusBadge(status: project.statusProject),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                      decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(4)),
                      child: Text(project.namaKategori, style: const TextStyle(fontSize: 10, color: AppColors.textSecondary, fontWeight: FontWeight.w600)),
                    ),
                    const SizedBox(width: 8),
                    const Icon(Icons.location_on, size: 14, color: AppColors.textMuted),
                    const SizedBox(width: 2),
                    Expanded(child: Text(project.lokasi, style: const TextStyle(fontSize: 12, color: AppColors.textMuted), maxLines: 1, overflow: TextOverflow.ellipsis)),
                  ],
                ),
                const SizedBox(height: 16),
                
                // Mock MRV Status & Sell through
                if (project.statusProject == 'verified') ...[
                  const Text('Tokens Sold', style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      Expanded(
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(4),
                          child: const LinearProgressIndicator(value: 0.65, backgroundColor: AppColors.border, valueColor: AlwaysStoppedAnimation(AppColors.primary), minHeight: 6),
                        ),
                      ),
                      const SizedBox(width: 8),
                      const Text('65%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.primary)),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text('Revenue: Rp 25.000.000', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.transfer)),
                ] else ...[
                  const Row(
                    children: [
                      Icon(Icons.info_outline, size: 14, color: AppColors.pending),
                      SizedBox(width: 6),
                      Text('MRV Status: Pending verification', style: TextStyle(fontSize: 12, color: AppColors.pending, fontWeight: FontWeight.w500)),
                    ],
                  ),
                ],
              ],
            ),
          ),
          Divider(height: 1, color: AppColors.border.withValues(alpha: 0.5)),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            child: Row(
              children: [
                Expanded(
                  child: TextButton.icon(
                    onPressed: onUpdateMrv,
                    icon: const Icon(Icons.upload_file, size: 18),
                    label: const Text('Update MRV'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextButton.icon(
                    onPressed: project.statusProject == 'verified' ? onViewInMarket : null,
                    icon: const Icon(Icons.storefront, size: 18),
                    label: const Text('Marketplace'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
