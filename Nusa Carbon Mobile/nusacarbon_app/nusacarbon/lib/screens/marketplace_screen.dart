import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../constants/app_colors.dart';
import '../providers/marketplace_provider.dart';
import '../providers/account_provider.dart';
import '../models/listing.dart';

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
  ];
  bool _showSearch = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final userId = context.read<AccountProvider>().currentUserId;
      context.read<MarketplaceProvider>().loadListings(userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<MarketplaceProvider>();

    return Scaffold(
      appBar: AppBar(
        title:
            _showSearch
                ? TextField(
                  autofocus: true,
                  decoration: const InputDecoration(
                    hintText: 'Search marketplace...',
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
                        final userId =
                            context.read<AccountProvider>().currentUserId;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(category),
                            selected: isSelected,
                            onSelected: (selected) {
                              provider.setCategory(
                                category == 'All' ? null : category,
                                userId,
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

                  // ─── Listings Grid ────────────────────────────────────
                  Expanded(
                    child:
                        provider.isLoading
                            ? const Center(child: CircularProgressIndicator())
                            : provider.filteredListings.isEmpty
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
                                        ? 'Could not load listings.\nCheck your connection.'
                                        : 'No listings found.',
                                    textAlign: TextAlign.center,
                                    style: const TextStyle(
                                      color: AppColors.textMuted,
                                    ),
                                  ),
                                  if (provider.error != null) ...[
                                    const SizedBox(height: 12),
                                    TextButton(
                                      onPressed: () {
                                        final userId =
                                            context
                                                .read<AccountProvider>()
                                                .currentUserId;
                                        provider.loadListings(userId);
                                      },
                                      child: const Text('Retry'),
                                    ),
                                  ],
                                ],
                              ),
                            )
                            : GridView.builder(
                              padding: const EdgeInsets.all(16),
                              gridDelegate:
                                  const SliverGridDelegateWithFixedCrossAxisCount(
                                    crossAxisCount: 2,
                                    childAspectRatio: 0.7,
                                    crossAxisSpacing: 16,
                                    mainAxisSpacing: 16,
                                  ),
                              itemCount: provider.filteredListings.length,
                              itemBuilder: (context, index) {
                                final listing =
                                    provider.filteredListings[index];
                                return _ListingCard(
                                  listing: listing,
                                  onTap:
                                      () => context.go(
                                        '/project/${listing.idProject}',
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
                ListTile(
                  title: const Text('Newest'),
                  trailing:
                      provider.sortBy == 'newest'
                          ? const Icon(Icons.check, color: AppColors.primary)
                          : null,
                  onTap: () {
                    provider.setSortBy('newest');
                    Navigator.pop(context);
                  },
                ),
                ListTile(
                  title: const Text('Price (Low to High)'),
                  trailing:
                      provider.sortBy == 'price_low'
                          ? const Icon(Icons.check, color: AppColors.primary)
                          : null,
                  onTap: () {
                    provider.setSortBy('price_low');
                    Navigator.pop(context);
                  },
                ),
                ListTile(
                  title: const Text('Price (High to Low)'),
                  trailing:
                      provider.sortBy == 'price_high'
                          ? const Icon(Icons.check, color: AppColors.primary)
                          : null,
                  onTap: () {
                    provider.setSortBy('price_high');
                    Navigator.pop(context);
                  },
                ),
              ],
            ),
          ),
    );
  }
}

class _ListingCard extends StatelessWidget {
  final Listing listing;
  final VoidCallback onTap;

  const _ListingCard({required this.listing, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final idr = NumberFormat.currency(
      locale: 'id_ID',
      symbol: 'Rp ',
      decimalDigits: 0,
    );
    final fmt = NumberFormat('#,###');

    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.06),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image
            Stack(
              children: [
                CachedNetworkImage(
                  imageUrl: listing.imageUrl ?? '',
                  height: 100,
                  width: double.infinity,
                  fit: BoxFit.cover,
                  placeholder:
                      (_, __) => Container(
                        height: 100,
                        decoration: const BoxDecoration(
                          gradient: LinearGradient(
                            colors: [Color(0xFFD1FAE5), Color(0xFFCCFBF1)],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        child: const Center(
                          child: Icon(Icons.eco, color: AppColors.primary),
                        ),
                      ),
                  errorWidget:
                      (_, __, ___) => Container(
                        height: 100,
                        color: const Color(0xFFECFDF5),
                        child: const Center(
                          child: Icon(Icons.eco, color: AppColors.primary),
                        ),
                      ),
                ),
                if (listing.namaKategori != null)
                  Positioned(
                    top: 8,
                    left: 8,
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 3,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.9),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        listing.namaKategori!,
                        style: const TextStyle(
                          fontSize: 9,
                          fontWeight: FontWeight.bold,
                          color: AppColors.primary,
                        ),
                      ),
                    ),
                  ),
              ],
            ),

            // Content
            Padding(
              padding: const EdgeInsets.all(10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    listing.namaProject,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      const Icon(
                        Icons.location_on,
                        size: 12,
                        color: AppColors.textMuted,
                      ),
                      const SizedBox(width: 2),
                      Expanded(
                        child: Text(
                          listing.lokasi ?? 'Indonesia',
                          style: const TextStyle(
                            fontSize: 10,
                            color: AppColors.textMuted,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                  const Spacer(),
                  Text(
                    idr.format(listing.hargaPerToken),
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: AppColors.primary,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    'Available: ${fmt.format(listing.jumlahToken)} tCO₂e',
                    style: const TextStyle(
                      fontSize: 10,
                      color: AppColors.textSecondary,
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
}
