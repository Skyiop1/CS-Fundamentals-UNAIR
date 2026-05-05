import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../constants/app_colors.dart';
import '../providers/marketplace_provider.dart';
import '../models/carbon_project.dart';

class MarketplaceScreen extends StatefulWidget {
  const MarketplaceScreen({super.key});

  @override
  State<MarketplaceScreen> createState() => _MarketplaceScreenState();
}

class _MarketplaceScreenState extends State<MarketplaceScreen> {
  final _categories = [
    'All',
    'Hutan',
    'Mangrove',
    'Energi Terbarukan',
    'Blue Carbon',
    'Lahan Gambut',
  ];
  bool _showSearch = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<MarketplaceProvider>().loadProjects();
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<MarketplaceProvider>();

    return Scaffold(
      appBar: AppBar(
        leading:
            Navigator.canPop(context)
                ? IconButton(
                  icon: const Icon(Icons.arrow_back),
                  onPressed: () => Navigator.of(context).pop(),
                )
                : null,
        title:
            _showSearch
                ? TextField(
                  autofocus: true,
                  decoration: const InputDecoration(
                    hintText: 'Search projects...',
                    border: InputBorder.none,
                  ),
                  onChanged: provider.setSearch,
                )
                : const Text('Marketplace'),
        actions: [
          IconButton(
            icon: Icon(_showSearch ? Icons.close : Icons.search),
            onPressed: () {
              setState(() => _showSearch = !_showSearch);
              if (!_showSearch) provider.setSearch('');
            },
          ),
          IconButton(
            icon: const Icon(Icons.sort),
            onPressed: () => _showSortOptions(context, provider),
          ),
        ],
      ),
      body:
          provider.isLoading
              ? const Center(child: CircularProgressIndicator())
              : Column(
                children: [
                  // ─── Categories Filter ────────────────────────────────
                  SizedBox(
                    height: 50,
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      itemCount: _categories.length,
                      itemBuilder: (context, index) {
                        final category = _categories[index];
                        final isSelected =
                            (provider.categoryFilter == null &&
                                category == 'All') ||
                            (provider.categoryFilter == category);
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(category),
                            selected: isSelected,
                            onSelected: (selected) {
                              provider.setCategory(
                                category == 'All' ? null : category,
                              );
                            },
                            selectedColor: AppColors.primary,
                            labelStyle: TextStyle(
                              color:
                                  isSelected
                                      ? Colors.white
                                      : AppColors.textSecondary,
                              fontWeight:
                                  isSelected
                                      ? FontWeight.w600
                                      : FontWeight.normal,
                            ),
                          ),
                        );
                      },
                    ),
                  ),

                  // ─── Projects List ────────────────────────────────────
                  Expanded(
                    child:
                        provider.filteredProjects.isEmpty
                            ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(
                                    Icons.search_off,
                                    size: 48,
                                    color: AppColors.textMuted,
                                  ),
                                  const SizedBox(height: 12),
                                  Text(
                                    provider.error != null
                                        ? 'Could not load projects.\nCheck your connection.'
                                        : 'No projects found.',
                                    textAlign: TextAlign.center,
                                    style: const TextStyle(
                                      color: AppColors.textMuted,
                                    ),
                                  ),
                                  if (provider.error != null) ...[
                                    const SizedBox(height: 12),
                                    TextButton(
                                      onPressed: () => provider.loadProjects(),
                                      child: const Text('Retry'),
                                    ),
                                  ],
                                ],
                              ),
                            )
                            : ListView.builder(
                              padding: const EdgeInsets.all(16),
                              itemCount: provider.filteredProjects.length,
                              itemBuilder: (context, index) {
                                final project =
                                    provider.filteredProjects[index];
                                return _ProjectMarketCard(
                                  project: project,
                                  onTap:
                                      () => context.push(
                                        '/project/${project.idProject}',
                                      ),
                                );
                              },
                            ),
                  ),
                ],
              ),
    );
  }

  void _showSortOptions(BuildContext context, MarketplaceProvider provider) {
    showModalBottomSheet(
      context: context,
      builder:
          (context) => SafeArea(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Padding(
                  padding: EdgeInsets.all(16),
                  child: Text(
                    'Sort by',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
                _SortTile(
                  title: 'Newest',
                  value: 'newest',
                  current: provider.sortBy,
                  onTap: () {
                    provider.setSortBy('newest');
                    Navigator.pop(context);
                  },
                ),
                _SortTile(
                  title: 'Name (A–Z)',
                  value: 'name_az',
                  current: provider.sortBy,
                  onTap: () {
                    provider.setSortBy('name_az');
                    Navigator.pop(context);
                  },
                ),
                _SortTile(
                  title: 'Name (Z–A)',
                  value: 'name_za',
                  current: provider.sortBy,
                  onTap: () {
                    provider.setSortBy('name_za');
                    Navigator.pop(context);
                  },
                ),
                _SortTile(
                  title: 'Area (Largest)',
                  value: 'area_large',
                  current: provider.sortBy,
                  onTap: () {
                    provider.setSortBy('area_large');
                    Navigator.pop(context);
                  },
                ),
                _SortTile(
                  title: 'Area (Smallest)',
                  value: 'area_small',
                  current: provider.sortBy,
                  onTap: () {
                    provider.setSortBy('area_small');
                    Navigator.pop(context);
                  },
                ),
              ],
            ),
          ),
    );
  }
}

// ─── Sort Tile helper ───────────────────────────────────────────────────────

class _SortTile extends StatelessWidget {
  final String title;
  final String value;
  final String current;
  final VoidCallback onTap;

  const _SortTile({
    required this.title,
    required this.value,
    required this.current,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(title),
      trailing:
          current == value
              ? const Icon(Icons.check, color: AppColors.primary)
              : null,
      onTap: onTap,
    );
  }
}

// ─── Project Market Card ────────────────────────────────────────────────────

class _ProjectMarketCard extends StatelessWidget {
  final CarbonProject project;
  final VoidCallback onTap;

  const _ProjectMarketCard({required this.project, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final fmt = NumberFormat('#,###');
    final colors = AppColors.projectTypeColors(project.namaKategori);

    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.06),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ─── Image header ────────────────────────────────────────
            Stack(
              children: [
                CachedNetworkImage(
                  imageUrl: project.imageUrl ?? '',
                  height: 150,
                  width: double.infinity,
                  fit: BoxFit.cover,
                  placeholder:
                      (_, __) => Container(
                        height: 150,
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              colors.bg,
                              colors.bg.withValues(alpha: 0.5),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        child: Center(
                          child: Icon(
                            _categoryIcon(project.namaKategori),
                            color: colors.text,
                            size: 48,
                          ),
                        ),
                      ),
                  errorWidget:
                      (_, __, ___) => Container(
                        height: 150,
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              colors.bg,
                              colors.bg.withValues(alpha: 0.5),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        child: Center(
                          child: Icon(
                            _categoryIcon(project.namaKategori),
                            color: colors.text,
                            size: 48,
                          ),
                        ),
                      ),
                ),
                // Category badge
                Positioned(
                  top: 12,
                  left: 12,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 5,
                    ),
                    decoration: BoxDecoration(
                      color: colors.bg,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          _categoryIcon(project.namaKategori),
                          size: 14,
                          color: colors.text,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          project.namaKategori,
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: colors.text,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                // Status badge
                Positioned(
                  top: 12,
                  right: 12,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 5,
                    ),
                    decoration: BoxDecoration(
                      color: AppColors.verifiedBg,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.verified,
                          size: 14,
                          color: AppColors.verified,
                        ),
                        SizedBox(width: 4),
                        Text(
                          'Verified',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: AppColors.verified,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),

            // ─── Content ─────────────────────────────────────────────
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Title
                  Text(
                    project.namaProject,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 8),

                  // Location & Owner row
                  Row(
                    children: [
                      const Icon(
                        Icons.location_on,
                        size: 14,
                        color: AppColors.textMuted,
                      ),
                      const SizedBox(width: 4),
                      Expanded(
                        child: Text(
                          project.lokasi,
                          style: const TextStyle(
                            fontSize: 12,
                            color: AppColors.textMuted,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      if (project.ownerName != null) ...[
                        const SizedBox(width: 12),
                        const Icon(
                          Icons.business,
                          size: 14,
                          color: AppColors.textMuted,
                        ),
                        const SizedBox(width: 4),
                        Flexible(
                          child: Text(
                            project.ownerName!,
                            style: const TextStyle(
                              fontSize: 12,
                              color: AppColors.textMuted,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Description
                  if (project.deskripsi != null &&
                      project.deskripsi!.isNotEmpty) ...[
                    Text(
                      project.deskripsi!,
                      style: const TextStyle(
                        fontSize: 13,
                        color: AppColors.textSecondary,
                        height: 1.5,
                      ),
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 12),
                  ],

                  // Metrics row
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.background,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Row(
                      children: [
                        _MetricItem(
                          icon: Icons.terrain,
                          label: 'Luas Lahan',
                          value: '${fmt.format(project.luasLahan)} ha',
                        ),
                        Container(
                          width: 1,
                          height: 30,
                          color: AppColors.border,
                          margin: const EdgeInsets.symmetric(horizontal: 12),
                        ),
                        _MetricItem(
                          icon: _categoryIcon(project.namaKategori),
                          label: 'Kategori',
                          value: project.namaKategori,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // View Details button
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      onPressed: onTap,
                      icon: const Icon(Icons.arrow_forward, size: 18),
                      label: const Text('Lihat Detail'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.primary,
                        side: const BorderSide(color: AppColors.primary),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                    ),
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
      case 'forest':
        return Icons.park;
      case 'mangrove':
        return Icons.eco;
      case 'energi terbarukan':
      case 'renewable energy':
        return Icons.solar_power;
      case 'blue carbon':
        return Icons.water;
      case 'lahan gambut':
      case 'peatland':
        return Icons.grass;
      default:
        return Icons.eco;
    }
  }
}

// ─── Metric Item ────────────────────────────────────────────────────────────

class _MetricItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _MetricItem({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Row(
        children: [
          Icon(icon, size: 18, color: AppColors.primary),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 10,
                    color: AppColors.textMuted,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
