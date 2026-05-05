import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../constants/app_colors.dart';
import '../providers/tokens_provider.dart';
import '../providers/account_provider.dart';

class TokensScreen extends StatefulWidget {
  const TokensScreen({super.key});
  @override
  State<TokensScreen> createState() => _TokensScreenState();
}

class _TokensScreenState extends State<TokensScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _tabs = ['All', 'Available', 'Retired', 'Listed'];
  bool _showSearch = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: _tabs.length, vsync: this);
    _tabController.addListener(() {
      if (!_tabController.indexIsChanging) {
        context.read<TokensProvider>().setTab(_tabs[_tabController.index]);
      }
    });
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final account = context.read<AccountProvider>();
      context
          .read<TokensProvider>()
          .loadTokens(account.currentUserId, isDeveloper: account.isDeveloper);
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<TokensProvider>();
    final fmt = NumberFormat('#,###');

    return Scaffold(
      appBar: AppBar(
        title: _showSearch
            ? TextField(
                autofocus: true,
                decoration: const InputDecoration(
                  hintText: 'Search projects...',
                  border: InputBorder.none,
                ),
                onChanged: provider.setSearch,
              )
            : const Text('My Tokens'),
        actions: [
          IconButton(
            icon: Icon(_showSearch ? Icons.close : Icons.search),
            onPressed: () {
              setState(() {
                _showSearch = !_showSearch;
                if (!_showSearch) provider.setSearch('');
              });
            },
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          tabs: _tabs.map((t) => Tab(text: t)).toList(),
        ),
      ),
      body: provider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                // Summary stats
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Expanded(
                        child: _StatCard(
                          label: 'Total Tokens',
                          value: '${fmt.format(provider.totalTokenCount)} tCO₂e',
                          icon: Icons.eco,
                          color: AppColors.primary,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _StatCard(
                          label: 'Active Projects',
                          value: '${provider.activeProjectCount}',
                          icon: Icons.folder_open,
                          color: AppColors.secondary,
                        ),
                      ),
                    ],
                  ),
                ),
                // Grouped token list
                Expanded(
                  child: provider.filteredGroups.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.token_outlined,
                                  size: 48, color: AppColors.textMuted),
                              const SizedBox(height: 12),
                              Text(
                                provider.error != null
                                    ? 'Could not load tokens.\nCheck your connection.'
                                    : 'No tokens found.',
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                    color: AppColors.textMuted),
                              ),
                              if (provider.error != null) ...[
                                const SizedBox(height: 12),
                                TextButton(
                                  onPressed: () {
                                    final account =
                                        context.read<AccountProvider>();
                                    provider.loadTokens(
                                        account.currentUserId);
                                  },
                                  child: const Text('Retry'),
                                ),
                              ],
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          itemCount: provider.filteredGroups.length,
                          itemBuilder: (_, i) {
                            final group = provider.filteredGroups[i];
                            return _TokenGroupCard(
                              group: group,
                              onTap: () =>
                                  context.push('/project/${group.idProject}'),
                            );
                          },
                        ),
                ),
              ],
            ),
    );
  }
}

// ─── Stat Card ──────────────────────────────────────────────────────────────

class _StatCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;
  const _StatCard(
      {required this.label,
      required this.value,
      required this.icon,
      required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, size: 20, color: color),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label,
                    style: const TextStyle(
                        fontSize: 11, color: AppColors.textMuted)),
                const SizedBox(height: 2),
                Text(value,
                    style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ─── Token Group Card ───────────────────────────────────────────────────────

class _TokenGroupCard extends StatelessWidget {
  final TokenProjectGroup group;
  final VoidCallback onTap;
  const _TokenGroupCard({required this.group, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final fmt = NumberFormat('#,###');
    final colors = AppColors.projectTypeColors(group.namaKategori);

    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
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
            // ─── Image header ──────────────────────────────────
            Stack(
              children: [
                ClipRRect(
                  borderRadius:
                      const BorderRadius.vertical(top: Radius.circular(14)),
                  child: CachedNetworkImage(
                    imageUrl: group.imageUrl ?? '',
                    height: 120,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    placeholder: (_, __) => Container(
                      height: 120,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [colors.bg, colors.bg.withValues(alpha: 0.5)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                      child: Center(
                        child: Icon(_categoryIcon(group.namaKategori),
                            color: colors.text, size: 40),
                      ),
                    ),
                    errorWidget: (_, __, ___) => Container(
                      height: 120,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [colors.bg, colors.bg.withValues(alpha: 0.5)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                      child: Center(
                        child: Icon(_categoryIcon(group.namaKategori),
                            color: colors.text, size: 40),
                      ),
                    ),
                  ),
                ),
                // Category badge
                Positioned(
                  top: 8,
                  left: 8,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: colors.bg,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(_categoryIcon(group.namaKategori),
                            size: 12, color: colors.text),
                        const SizedBox(width: 4),
                        Text(group.namaKategori,
                            style: TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.w600,
                                color: colors.text)),
                      ],
                    ),
                  ),
                ),
                // Verification standard
                Positioned(
                  top: 8,
                  right: 8,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.9),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Text(
                      _getVerificationStandard(group.namaKategori),
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

            // ─── Content ───────────────────────────────────────
            Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Project name
                  Text(
                    group.namaProject,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  // Location
                  Row(
                    children: [
                      const Icon(Icons.location_on,
                          size: 13, color: AppColors.textMuted),
                      const SizedBox(width: 3),
                      Text(group.lokasi,
                          style: const TextStyle(
                              fontSize: 12, color: AppColors.textMuted)),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Token amount
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFFECFDF5), Color(0xFFF0FDFA)],
                      ),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.eco,
                            size: 22, color: AppColors.primary),
                        const SizedBox(width: 10),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Your Holdings',
                                style: TextStyle(
                                    fontSize: 10,
                                    color: AppColors.textMuted)),
                            Text(
                              '${fmt.format(group.totalTokens)} tCO₂e',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: AppColors.primary,
                              ),
                            ),
                          ],
                        ),
                        const Spacer(),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            const Text('Vintage',
                                style: TextStyle(
                                    fontSize: 10,
                                    color: AppColors.textMuted)),
                            Text(
                              '${group.vintageYear}',
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: AppColors.textPrimary,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 10),

                  // Status breakdown
                  Row(
                    children: [
                      if (group.availableCount > 0)
                        _StatusChip(
                            label: 'Available',
                            count: group.availableCount,
                            color: AppColors.verified),
                      if (group.listedCount > 0)
                        _StatusChip(
                            label: 'Listed',
                            count: group.listedCount,
                            color: AppColors.transfer),
                      if (group.soldCount > 0)
                        _StatusChip(
                            label: 'Sold',
                            count: group.soldCount,
                            color: AppColors.pending),
                      if (group.retiredCount > 0)
                        _StatusChip(
                            label: 'Retired',
                            count: group.retiredCount,
                            color: AppColors.rejected),
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

  IconData _categoryIcon(String category) {
    switch (category.toLowerCase()) {
      case 'hutan':
        return Icons.park;
      case 'mangrove':
        return Icons.eco;
      case 'energi terbarukan':
        return Icons.solar_power;
      case 'blue carbon':
        return Icons.water;
      case 'lahan gambut':
        return Icons.grass;
      default:
        return Icons.eco;
    }
  }

  String _getVerificationStandard(String category) {
    if (category.toLowerCase().contains('hutan') ||
        category.toLowerCase().contains('forest')) {
      return 'GOLD STANDARD';
    }
    return 'VERRA VCS';
  }
}

// ─── Status Chip ────────────────────────────────────────────────────────────

class _StatusChip extends StatelessWidget {
  final String label;
  final int count;
  final Color color;
  const _StatusChip(
      {required this.label, required this.count, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 6,
            height: 6,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
          ),
          const SizedBox(width: 4),
          Text('$count $label',
              style: TextStyle(
                  fontSize: 10, fontWeight: FontWeight.w600, color: color)),
        ],
      ),
    );
  }
}
