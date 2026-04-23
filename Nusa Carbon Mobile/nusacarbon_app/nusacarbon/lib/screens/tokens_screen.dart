import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../providers/tokens_provider.dart';
import '../providers/account_provider.dart';
import '../widgets/token_card.dart';

class TokensScreen extends StatefulWidget {
  const TokensScreen({super.key});
  @override
  State<TokensScreen> createState() => _TokensScreenState();
}

class _TokensScreenState extends State<TokensScreen> with SingleTickerProviderStateMixin {
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
      context.read<TokensProvider>().loadTokens(account.currentUserId, isDeveloper: account.isDeveloper);
    });
  }

  @override
  void dispose() { _tabController.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<TokensProvider>();
    final fmt = NumberFormat('#,###');

    return Scaffold(
      appBar: AppBar(
        title: _showSearch
            ? TextField(autofocus: true, decoration: const InputDecoration(hintText: 'Search projects...', border: InputBorder.none), onChanged: provider.setSearch)
            : const Text('My Tokens'),
        actions: [
          IconButton(icon: Icon(_showSearch ? Icons.close : Icons.search), onPressed: () {
            setState(() { _showSearch = !_showSearch; if (!_showSearch) provider.setSearch(''); });
          }),
        ],
        bottom: TabBar(controller: _tabController, tabs: _tabs.map((t) => Tab(text: t)).toList()),
      ),
      body: provider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(children: [
              // Summary stats
              Padding(
                padding: const EdgeInsets.all(16),
                child: Row(children: [
                  Expanded(child: _StatCard(label: 'Total Tokens', value: '${fmt.format(provider.totalTokenCount)} tCO₂e')),
                  const SizedBox(width: 12),
                  Expanded(child: _StatCard(label: 'Active Projects', value: '${provider.activeProjectCount} (+1 pending)')),
                ]),
              ),
              // Token list
              Expanded(
                child: provider.filteredTokens.isEmpty
                    ? const Center(child: Text('No tokens found', style: TextStyle(color: AppColors.textMuted)))
                    : ListView.builder(
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        itemCount: provider.filteredTokens.length,
                        itemBuilder: (_, i) {
                          final token = provider.filteredTokens[i];
                          return TokenCard(token: token, onTap: () => context.go('/tokens/${token.idToken}'));
                        },
                      ),
              ),
            ]),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String label; final String value;
  const _StatCard({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12), boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 8, offset: const Offset(0, 2))]),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
      ]),
    );
  }
}
