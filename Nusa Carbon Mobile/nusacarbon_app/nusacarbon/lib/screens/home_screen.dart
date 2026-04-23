import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../data/mock_data.dart';
import '../providers/home_provider.dart';
import '../providers/account_provider.dart';
import '../widgets/portfolio_hero_card.dart';
import '../widgets/price_chart_widget.dart';
import '../widgets/project_card.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final userId = context.read<AccountProvider>().currentUserId;
      context.read<HomeProvider>().loadData(userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final account = context.watch<AccountProvider>();
    final home = context.watch<HomeProvider>();

    return Scaffold(
      appBar: AppBar(
        title: Row(mainAxisSize: MainAxisSize.min, children: [
          Container(
            width: 32, height: 32,
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(8), gradient: AppColors.logoGradient),
            child: const Icon(Icons.eco, color: Colors.white, size: 18),
          ),
          const SizedBox(width: 8),
          const Text('NusaCarbon', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 18, color: AppColors.primary)),
        ]),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
            child: TextButton.icon(
              onPressed: () => account.toggleMode(),
              icon: Icon(account.isDeveloper ? Icons.business_center : Icons.person_outline, size: 16),
              label: Text(account.isDeveloper ? 'DEV' : 'INV', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
              style: TextButton.styleFrom(
                 foregroundColor: AppColors.primary,
                 backgroundColor: AppColors.primary.withValues(alpha: 0.1),
                 padding: const EdgeInsets.symmetric(horizontal: 12),
                 minimumSize: Size.zero,
                 shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
              ),
            ),
          ),
          IconButton(icon: Badge(label: const Text('3'), child: const Icon(Icons.notifications_outlined)), onPressed: () {}),
          IconButton(icon: const Icon(Icons.settings), onPressed: () {}),
        ],
      ),
      body: home.isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: () => home.loadData(account.currentUserId),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  // Portfolio Hero
                  PortfolioHeroCard(
                    portfolioValue: home.portfolioValue,
                    totalTokens: home.totalTokens,
                    monthlyChange: home.monthlyChange,
                    onPortfolioTap: () => context.go('/wallet'),
                  ),
                  const SizedBox(height: 20),
                  // Price Chart
                  PriceChartWidget(
                    prices: home.priceData,
                    labels: home.priceLabels,
                    currentPrice: MockData.tokenPriceIdr,
                    percentageChange: 8.2,
                  ),
                  const SizedBox(height: 20),
                  // Quick Actions
                  _buildQuickActions(context, account.currentMode),
                  const SizedBox(height: 24),
                  // Active Projects
                  Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                    const Text('Active Projects', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                    TextButton(onPressed: () => context.go('/marketplace'), child: const Text('View All')),
                  ]),
                  const SizedBox(height: 8),
                  SizedBox(
                    height: 210,
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: home.activeProjects.length,
                      itemBuilder: (_, i) {
                        final p = home.activeProjects[i];
                        final tokens = i == 0 ? '12,500' : '7,500';
                        return ProjectCard(project: p, tokensHeld: tokens, onTap: () => context.go('/project/${p.idProject}'));
                      },
                    ),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
    );
  }

  Widget _buildQuickActions(BuildContext context, AccountMode mode) {
    return Row(children: [
      if (mode == AccountMode.developer)
        _ActionBtn(icon: Icons.add_circle_outline, label: 'Tokenize', color: AppColors.primary, onTap: () => context.go('/dashboard/owner')),
      if (mode == AccountMode.developer) const SizedBox(width: 12),
      Expanded(child: _ActionBtn(icon: Icons.local_fire_department, label: 'Retire', color: AppColors.rejected, onTap: () => context.go('/tokens'))),
      const SizedBox(width: 12),
      Expanded(child: _ActionBtn(icon: Icons.swap_horiz, label: 'Transfer', color: AppColors.transfer, onTap: () => context.go('/wallet'))),
      const SizedBox(width: 12),
      Expanded(child: _ActionBtn(icon: Icons.store, label: 'Market', color: AppColors.secondary, onTap: () => context.go('/marketplace'))),
    ]);
  }
}

class _ActionBtn extends StatelessWidget {
  final IconData icon; final String label; final Color color; final VoidCallback onTap;
  const _ActionBtn({required this.icon, required this.label, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(color: color.withValues(alpha: 0.08), borderRadius: BorderRadius.circular(12)),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 6),
          Text(label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: color)),
        ]),
      ),
    );
  }
}
