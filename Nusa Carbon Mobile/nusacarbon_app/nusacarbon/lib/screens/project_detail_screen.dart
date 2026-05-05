import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../models/carbon_project.dart';
import '../models/listing.dart';
import '../models/blockchain_tx.dart';
import '../models/mrv_report.dart';
import '../providers/account_provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import '../widgets/status_badge.dart';
import '../widgets/mrv_chart.dart';
import '../widgets/blockchain_tx_tile.dart';
import '../widgets/buy_token_widget.dart';

// ─── Data holder ─────────────────────────────────────────────────────────────

/// Bundles all data fetched in parallel for this screen.
class _ProjectData {
  final CarbonProject project;

  /// Active marketplace listing for this project, or null if none / sold-out.
  final Listing? listing;

  /// Blockchain ledger entries scoped to this project's token mints/transfers.
  final List<BlockchainTx> ledger;

  /// All MRV reports submitted for this project.
  final List<MrvReport> mrvReports;

  const _ProjectData({
    required this.project,
    this.listing,
    required this.ledger,
    required this.mrvReports,
  });
}

// ─── Screen ───────────────────────────────────────────────────────────────────

class ProjectDetailScreen extends StatelessWidget {
  final int projectId;
  const ProjectDetailScreen({super.key, required this.projectId});

  // ── Data loading ────────────────────────────────────────────────────────────

  Future<_ProjectData?> _fetchAll() async {
    try {
      final api = ApiService();

      // Fire all four requests in parallel to minimise wait time.
      final results = await Future.wait([
        api.getProjectById(projectId), // [0] project detail
        api.getListings(), // [1] marketplace (filter locally)
        api.getBlockchainLedger(projectId: projectId), // [2] ledger for project
        api.getMrvByProject(projectId), // [3] MRV reports
      ]);

      // ── [0] Project ─────────────────────────────────────────────────
      final projectRes = results[0];
      if (projectRes.statusCode != 200) return null;
      final pRaw = projectRes.data['data'];
      if (pRaw == null) return null;
      final project = CarbonProject.fromJson(pRaw as Map<String, dynamic>);

      // ── [1] Listing ─────────────────────────────────────────────────
      Listing? listing;
      final listingRes = results[1];
      if (listingRes.statusCode == 200) {
        final raw = listingRes.data['data'] as List?;
        if (raw != null) {
          final all =
              raw
                  .map((l) => Listing.fromJson(l as Map<String, dynamic>))
                  .toList();
          final matches = all.where(
            (l) => l.idProject == projectId && l.statusListing == 'active',
          );
          if (matches.isNotEmpty) listing = matches.first;
        }
      }

      // ── [2] Ledger ──────────────────────────────────────────────────
      final ledger = <BlockchainTx>[];
      final ledgerRes = results[2];
      if (ledgerRes.statusCode == 200) {
        final raw = ledgerRes.data['data'] as List?;
        if (raw != null) {
          ledger.addAll(
            raw.map((e) => BlockchainTx.fromJson(e as Map<String, dynamic>)),
          );
        }
      }

      // ── [3] MRV reports ─────────────────────────────────────────────
      final mrvReports = <MrvReport>[];
      final mrvRes = results[3];
      if (mrvRes.statusCode == 200) {
        final raw = mrvRes.data['data'] as List?;
        if (raw != null) {
          mrvReports.addAll(
            raw.map((m) => MrvReport.fromJson(m as Map<String, dynamic>)),
          );
        }
      }

      return _ProjectData(
        project: project,
        listing: listing,
        ledger: ledger,
        mrvReports: mrvReports,
      );
    } catch (e) {
      debugPrint('ProjectDetailScreen._fetchAll error: $e');
      return null;
    }
  }

  // ── Build ───────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final buyerUserId = context.read<AccountProvider>().currentUserId;
    final role = context.read<AuthProvider>().role ?? 'buyer';
    // Only buyers / investors see the purchase widget.
    final canBuy = role == 'buyer' || role == 'investor';

    return FutureBuilder<_ProjectData?>(
      future: _fetchAll(),
      builder: (context, snapshot) {
        // ── Loading ──────────────────────────────────────────────────
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }

        // ── Error / not found ────────────────────────────────────────
        final data = snapshot.data;
        if (data == null) {
          return Scaffold(
            appBar: AppBar(title: const Text('Project')),
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    size: 48,
                    color: AppColors.textMuted,
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'Could not load project.\nCheck your connection.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: AppColors.textMuted),
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('Go Back'),
                  ),
                ],
              ),
            ),
          );
        }

        // ── Main view ────────────────────────────────────────────────
        final project = data.project;
        final listing = data.listing;
        final isVerified = project.statusProject == 'verified';
        final hasActiveListing = listing != null;

        return DefaultTabController(
          length: 3,
          child: Scaffold(
            appBar: AppBar(
              leading:
                  Navigator.canPop(context)
                      ? IconButton(
                        icon: const Icon(Icons.arrow_back),
                        onPressed: () => Navigator.of(context).pop(),
                      )
                      : null,
              title: Text(project.namaProject, overflow: TextOverflow.ellipsis),
              actions: [
                IconButton(icon: const Icon(Icons.share), onPressed: () {}),
              ],
            ),
            body: Column(
              children: [
                // ── Scrollable content + tabs ────────────────────────
                Expanded(
                  child: NestedScrollView(
                    headerSliverBuilder:
                        (context, _) => [
                          SliverToBoxAdapter(
                            child: _ProjectHeader(project: project),
                          ),
                          SliverPersistentHeader(
                            pinned: true,
                            delegate: _TabBarDelegate(
                              const TabBar(
                                tabs: [
                                  Tab(text: 'dMRV Data'),
                                  Tab(text: 'Ledger'),
                                  Tab(text: 'Info'),
                                ],
                              ),
                            ),
                          ),
                        ],
                    body: TabBarView(
                      children: [
                        _MrvTab(mrvReports: data.mrvReports),
                        _LedgerTab(ledger: data.ledger),
                        _InfoTab(project: project, listing: listing),
                      ],
                    ),
                  ),
                ),

                // ── Sticky buy widget ────────────────────────────────
                // Shown only when: project is verified, has an active
                // listing, and the current user is a buyer / investor.
                if (isVerified && hasActiveListing && canBuy)
                  BuyTokenWidget(
                    idListing: listing.idListing,
                    buyerUserId: buyerUserId,
                    projectName: project.namaProject,
                    vintageYear: listing.createdAt.year,
                    pricePerToken: listing.hargaPerToken,
                    maxAvailable: listing.jumlahToken,
                  ),
              ],
            ),
          ),
        );
      },
    );
  }
}

// ─── Project header (hero image + title + description) ───────────────────────

class _ProjectHeader extends StatelessWidget {
  final CarbonProject project;
  const _ProjectHeader({required this.project});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Hero image
        Stack(
          children: [
            CachedNetworkImage(
              imageUrl: project.imageUrl ?? '',
              height: 220,
              width: double.infinity,
              fit: BoxFit.cover,
              placeholder:
                  (_, __) => Container(
                    height: 220,
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: [Color(0xFFD1FAE5), Color(0xFFCCFBF1)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                    ),
                    child: const Center(
                      child: Icon(
                        Icons.eco,
                        color: AppColors.primary,
                        size: 48,
                      ),
                    ),
                  ),
              errorWidget:
                  (_, __, ___) => Container(
                    height: 220,
                    color: const Color(0xFFECFDF5),
                    child: const Center(
                      child: Icon(
                        Icons.eco,
                        color: AppColors.primary,
                        size: 48,
                      ),
                    ),
                  ),
            ),
            // Status badge
            Positioned(
              top: 16,
              left: 16,
              child: StatusBadge(
                status:
                    project.statusProject == 'verified'
                        ? 'active'
                        : project.statusProject,
              ),
            ),
            // Verification standard badge
            Positioned(
              top: 16,
              right: 16,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.9),
                  borderRadius: BorderRadius.circular(4),
                  border: Border.all(color: AppColors.border, width: 0.5),
                ),
                child: Text(
                  _verificationStandard(project.namaKategori),
                  style: const TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textSecondary,
                  ),
                ),
              ),
            ),
          ],
        ),

        // Title + location + description
        Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                project.namaProject,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(
                    Icons.location_on,
                    size: 16,
                    color: AppColors.textMuted,
                  ),
                  const SizedBox(width: 4),
                  Expanded(
                    child: Text(
                      project.lokasi,
                      style: const TextStyle(
                        fontSize: 14,
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ),
                ],
              ),
              if (project.deskripsi != null &&
                  project.deskripsi!.isNotEmpty) ...[
                const SizedBox(height: 16),
                Text(
                  project.deskripsi!,
                  style: const TextStyle(
                    fontSize: 14,
                    color: AppColors.textSecondary,
                    height: 1.5,
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }

  String _verificationStandard(String category) {
    final c = category.toLowerCase();
    if (c.contains('hutan') || c.contains('forest')) return 'GOLD STANDARD';
    return 'VERRA VCS';
  }
}

// ─── dMRV Data tab ────────────────────────────────────────────────────────────

class _MrvTab extends StatelessWidget {
  final List<MrvReport> mrvReports;
  const _MrvTab({required this.mrvReports});

  @override
  Widget build(BuildContext context) {
    if (mrvReports.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.bar_chart, size: 48, color: AppColors.textMuted),
              SizedBox(height: 12),
              Text(
                'No MRV data submitted yet.',
                style: TextStyle(color: AppColors.textMuted),
              ),
            ],
          ),
        ),
      );
    }

    // Sort oldest → newest for the chart
    final sorted = List<MrvReport>.from(mrvReports)
      ..sort((a, b) => a.createdAt.compareTo(b.createdAt));

    final chartData = sorted.map((m) => m.estimasiCo2e ?? 0.0).toList();
    final labels = sorted.map((m) => m.periodeMrv).toList();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        MrvChart(
          data: chartData,
          labels: labels,
          satelliteConfidence: List.filled(chartData.length, 0.92),
          aiScore: List.filled(chartData.length, 0.88),
        ),
        const SizedBox(height: 20),
        const Text(
          'MRV Reports',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 12),
        // Show newest first in the list
        ...sorted.reversed.map((m) => _MrvReportTile(mrv: m)),
      ],
    );
  }
}

class _MrvReportTile extends StatelessWidget {
  final MrvReport mrv;
  const _MrvReportTile({required this.mrv});

  @override
  Widget build(BuildContext context) {
    final fmt = NumberFormat('#,###');
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          // Period badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: AppColors.verifiedBg,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              mrv.periodeMrv,
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: AppColors.primary,
              ),
            ),
          ),
          const SizedBox(width: 12),
          // Estimate + notes
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  mrv.estimasiCo2e != null
                      ? '${fmt.format(mrv.estimasiCo2e!.toInt())} tCO₂e'
                      : 'Pending measurement',
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                ),
                if (mrv.catatan != null && mrv.catatan!.isNotEmpty)
                  Text(
                    mrv.catatan!,
                    style: const TextStyle(
                      fontSize: 12,
                      color: AppColors.textSecondary,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          StatusBadge(status: mrv.statusMrv),
        ],
      ),
    );
  }
}

// ─── Blockchain Ledger tab ────────────────────────────────────────────────────

class _LedgerTab extends StatelessWidget {
  final List<BlockchainTx> ledger;
  const _LedgerTab({required this.ledger});

  @override
  Widget build(BuildContext context) {
    if (ledger.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.link_off, size: 48, color: AppColors.textMuted),
              SizedBox(height: 12),
              Text(
                'No ledger entries yet.',
                style: TextStyle(color: AppColors.textMuted),
              ),
            ],
          ),
        ),
      );
    }
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: ledger.length,
      itemBuilder: (_, index) => BlockchainTxTile(tx: ledger[index]),
    );
  }
}

// ─── Info tab ─────────────────────────────────────────────────────────────────

class _InfoTab extends StatelessWidget {
  final CarbonProject project;
  final Listing? listing;
  const _InfoTab({required this.project, this.listing});

  @override
  Widget build(BuildContext context) {
    final fmt = NumberFormat('#,###');
    final idr = NumberFormat.currency(
      locale: 'id_ID',
      symbol: 'Rp ',
      decimalDigits: 0,
    );

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _InfoRow('Project Owner', project.ownerName ?? 'PT Hijau Nusantara'),
        _InfoRow('Category', project.namaKategori),
        _InfoRow(
          'Land Area',
          '${fmt.format(project.luasLahan.toInt())} hectares',
        ),
        if (project.koordinatLat != null && project.koordinatLng != null)
          _InfoRow(
            'Coordinates',
            '${project.koordinatLat!.toStringAsFixed(4)}, '
                '${project.koordinatLng!.toStringAsFixed(4)}',
          ),
        _InfoRow(
          'Verification Standard',
          _verificationStandard(project.namaKategori),
        ),
        _InfoRow('Status', project.statusProject.toUpperCase()),
        _InfoRow(
          'Registered',
          '${_monthName(project.createdAt.month)} ${project.createdAt.year}',
        ),

        // Marketplace listing details
        if (listing != null) ...[
          const SizedBox(height: 16),
          const Divider(color: AppColors.border),
          const SizedBox(height: 12),
          const Text(
            'Marketplace Listing',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 12),
          _InfoRow('Listing ID', '#${listing!.idListing}'),
          _InfoRow('Price per Token', idr.format(listing!.hargaPerToken)),
          _InfoRow(
            'Available Tokens',
            '${fmt.format(listing!.jumlahToken)} tCO₂e',
          ),
          _InfoRow('Seller', listing!.sellerName),
          _InfoRow('Listing Status', listing!.statusListing.toUpperCase()),
        ],

        const SizedBox(height: 24),
        const Text(
          'Documents',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 8),
        const _DocTile('Validation Report', Icons.description),
        const _DocTile('MRV Methodology', Icons.science),
        const _DocTile('Project Design Document (PDD)', Icons.article),
        const SizedBox(height: 24),
      ],
    );
  }

  String _verificationStandard(String category) {
    final c = category.toLowerCase();
    if (c.contains('hutan') || c.contains('forest')) return 'GOLD STANDARD';
    return 'VERRA VCS';
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
}

// ─── Shared helper widgets ────────────────────────────────────────────────────

class _TabBarDelegate extends SliverPersistentHeaderDelegate {
  final TabBar tabBar;
  _TabBarDelegate(this.tabBar);

  @override
  double get minExtent => tabBar.preferredSize.height;
  @override
  double get maxExtent => tabBar.preferredSize.height;

  @override
  Widget build(
    BuildContext context,
    double shrinkOffset,
    bool overlapsContent,
  ) {
    return Container(color: Colors.white, child: tabBar);
  }

  @override
  bool shouldRebuild(_TabBarDelegate old) => false;
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;
  const _InfoRow(this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(fontSize: 14, color: AppColors.textMuted),
          ),
          const SizedBox(width: 16),
          Flexible(
            child: Text(
              value,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: AppColors.textPrimary,
              ),
              textAlign: TextAlign.end,
            ),
          ),
        ],
      ),
    );
  }
}

class _DocTile extends StatelessWidget {
  final String title;
  final IconData icon;
  const _DocTile(this.title, this.icon);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: AppColors.primary, size: 20),
      title: Text(title, style: const TextStyle(fontSize: 14)),
      trailing: const Icon(
        Icons.open_in_new,
        size: 16,
        color: AppColors.textMuted,
      ),
      onTap: () {},
      contentPadding: EdgeInsets.zero,
      dense: true,
    );
  }
}
