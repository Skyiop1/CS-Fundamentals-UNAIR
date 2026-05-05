import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../constants/app_colors.dart';
import '../data/mock_data.dart';
import '../models/carbon_token.dart';
import '../services/api_service.dart';
import '../services/blockchain_service.dart';
import '../widgets/status_badge.dart';
import '../widgets/blockchain_tx_tile.dart';
import '../widgets/mrv_chart.dart';

import '../widgets/retire_token_bottom_sheet.dart';

class TokenDetailScreen extends StatefulWidget {
  final int tokenId;
  const TokenDetailScreen({super.key, required this.tokenId});

  @override
  State<TokenDetailScreen> createState() => _TokenDetailScreenState();
}

class _TokenDetailScreenState extends State<TokenDetailScreen> {
  late Future<CarbonToken?> _tokenFuture;

  @override
  void initState() {
    super.initState();
    _tokenFuture = _fetchToken();
  }

  void _reloadToken() {
    setState(() {
      _tokenFuture = _fetchToken();
    });
  }

  Future<CarbonToken?> _fetchToken() async {
    if (ApiService.useMock) {
      await Future.delayed(const Duration(milliseconds: 300));
      return MockData.mockTokens.firstWhere(
        (t) => t.idToken == widget.tokenId,
        orElse: () => MockData.mockTokens.first,
      );
    }
    try {
      final res = await ApiService().getTokenById(widget.tokenId);
      if (res.statusCode == 200) {
        final tData = res.data['data'];
        if (tData != null) return CarbonToken.fromJson(tData);
      }
    } catch (e) {
      debugPrint('Error fetching token: $e');
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<CarbonToken?>(
      future: _tokenFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        final token = snapshot.data;
        if (token == null) {
          return Scaffold(appBar: AppBar(title: const Text('Not Found')), body: const Center(child: Text('Token not found.')));
        }

        final fmt = NumberFormat('#,###');
    final idr = NumberFormat.currency(locale: 'id_ID', symbol: 'Rp ', decimalDigits: 0);

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
          title: Text(token.namaProject, overflow: TextOverflow.ellipsis),
          actions: [
            IconButton(
              icon: const Icon(Icons.share),
              onPressed: () {},
            ),
          ],
        ),
        body: NestedScrollView(
          headerSliverBuilder: (_, __) => [
            SliverToBoxAdapter(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              // Info card
              Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Row(children: [StatusBadge(status: token.statusToken), const SizedBox(width: 8), Container(padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3), decoration: BoxDecoration(border: Border.all(color: AppColors.border), borderRadius: BorderRadius.circular(4)), child: Text('VERRA VCS', style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w600, color: AppColors.textSecondary)))]),
                const SizedBox(height: 12),
                Text(token.namaProject, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                const SizedBox(height: 6),
                Row(children: [const Icon(Icons.location_on, size: 14, color: AppColors.textMuted), const SizedBox(width: 4), Text(token.lokasi, style: const TextStyle(fontSize: 13, color: AppColors.textMuted))]),
                const SizedBox(height: 12),
                Row(children: [
                  _Chip('${fmt.format(token.amount?.toInt() ?? 0)} tCO₂e', Icons.eco),
                  const SizedBox(width: 8),
                  _Chip('${token.vintageYear}', Icons.calendar_today),
                  const Spacer(),
                  if (token.txMintHash != null) Text(BlockchainService.truncateHash(token.txMintHash!), style: const TextStyle(fontFamily: 'monospace', fontSize: 11, color: AppColors.textMuted)),
                ]),
                const SizedBox(height: 12),
                Text('Value: ${idr.format((token.amount ?? 0) * MockData.tokenPriceIdr)}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AppColors.primary)),
              ])),
            ])),
            const SliverToBoxAdapter(child: TabBar(tabs: [Tab(text: 'dMRV Data'), Tab(text: 'Ledger'), Tab(text: 'Info')])),
          ],
          body: TabBarView(children: [
            // dMRV Tab
            SingleChildScrollView(padding: const EdgeInsets.all(16), child: MrvChart(data: MockData.mrvQuarterlyData, labels: MockData.mrvQuarterLabels, satelliteConfidence: MockData.satelliteConfidence, aiScore: MockData.aiVerificationScore)),
            // Ledger Tab
            ListView.builder(padding: const EdgeInsets.all(16), itemCount: MockData.mockBlockchainTxs.length, itemBuilder: (_, i) => BlockchainTxTile(tx: MockData.mockBlockchainTxs[i])),
            // Info Tab
            SingleChildScrollView(padding: const EdgeInsets.all(16), child: _buildInfoTab(token)),
          ]),
        ),
        bottomNavigationBar: token.statusToken == 'available' ? _buildRetireBar(context, token) : null,
      ),
    );
    });
  }

  Widget _buildRetireBar(BuildContext context, CarbonToken token) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: AppColors.border)),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, -2))
        ],
      ),
      child: SafeArea(
        child: ElevatedButton.icon(
          onPressed: () {
            showModalBottomSheet(
              context: context,
              isScrollControlled: true,
              builder: (context) => RetireTokenBottomSheet(
                token: token,
                onSuccess: _reloadToken,
              ),
            );
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.rejected,
            padding: const EdgeInsets.symmetric(vertical: 16),
          ),
          icon: const Icon(Icons.outbox),
          label: const Text('Retire Token'),
        ),
      ),
    );
  }

  Widget _buildInfoTab(CarbonToken token) {
    final project = MockData.mockProjects.firstWhere((p) => p.idProject == token.idProject, orElse: () => MockData.mockProjects.first);
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      if (project.deskripsi != null) ...[const Text('Description', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AppColors.textPrimary)), const SizedBox(height: 8), Text(project.deskripsi!, style: const TextStyle(fontSize: 14, color: AppColors.textSecondary, height: 1.5)), const SizedBox(height: 16)],
      _InfoRow('Project Owner', 'PT Hijau Nusantara'),
      _InfoRow('Category', project.namaKategori),
      _InfoRow('Land Area', '${NumberFormat('#,###').format(project.luasLahan.toInt())} hectares'),
      if (project.koordinatLat != null) _InfoRow('Coordinates', '${project.koordinatLat}, ${project.koordinatLng}'),
      _InfoRow('Verification', 'Verra VCS'),
      _InfoRow('SDGs', '13 · 14 · 15'),
      const SizedBox(height: 16),
      const Text('Documents', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
      const SizedBox(height: 8),
      _DocTile('Validation Report', Icons.description),
      _DocTile('MRV Methodology', Icons.science),
      _DocTile('Project Design Document (PDD)', Icons.article),
    ]);
  }
}

class _Chip extends StatelessWidget {
  final String label; final IconData icon;
  const _Chip(this.label, this.icon);
  @override
  Widget build(BuildContext context) => Row(mainAxisSize: MainAxisSize.min, children: [Icon(icon, size: 12, color: AppColors.textMuted), const SizedBox(width: 3), Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary, fontWeight: FontWeight.w500))]);
}

class _InfoRow extends StatelessWidget {
  final String label; final String value;
  const _InfoRow(this.label, this.value);
  @override
  Widget build(BuildContext context) => Padding(padding: const EdgeInsets.only(bottom: 10), child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Text(label, style: const TextStyle(fontSize: 13, color: AppColors.textMuted)), Flexible(child: Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.textPrimary), textAlign: TextAlign.end))]));
}

class _DocTile extends StatelessWidget {
  final String title; final IconData icon;
  const _DocTile(this.title, this.icon);
  @override
  Widget build(BuildContext context) => ListTile(leading: Icon(icon, color: AppColors.primary), title: Text(title, style: const TextStyle(fontSize: 14)), trailing: const Icon(Icons.open_in_new, size: 16, color: AppColors.textMuted), onTap: () {}, contentPadding: EdgeInsets.zero, dense: true);
}
