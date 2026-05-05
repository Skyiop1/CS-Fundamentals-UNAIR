import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../providers/wallet_provider.dart';
import '../providers/account_provider.dart';
import '../services/blockchain_service.dart';
import '../widgets/blockchain_tx_tile.dart';

class WalletScreen extends StatefulWidget {
  const WalletScreen({super.key});
  @override
  State<WalletScreen> createState() => _WalletScreenState();
}

class _WalletScreenState extends State<WalletScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final userId = context.read<AccountProvider>().currentUserId;
      context.read<WalletProvider>().loadWallet(userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final wallet = context.watch<WalletProvider>();
    final fmt = NumberFormat('#,###');

    return Scaffold(
      appBar: AppBar(title: const Text('Wallet')),
      body: wallet.isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(padding: const EdgeInsets.all(16), children: [
              // Wallet address card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: AppColors.dark, borderRadius: BorderRadius.circular(12)),
                child: Row(children: [
                  Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('Connected Wallet', style: TextStyle(fontSize: 12, color: Colors.white.withValues(alpha: 0.7))),
                    const SizedBox(height: 4),
                    Text(BlockchainService.truncateHash(wallet.wallet?.walletAddress ?? ''), style: const TextStyle(fontFamily: 'monospace', fontSize: 16, color: Colors.white, fontWeight: FontWeight.w600, letterSpacing: 0.5)),
                  ])),
                  IconButton(icon: const Icon(Icons.copy_all, color: Colors.white, size: 20), onPressed: () { Clipboard.setData(ClipboardData(text: wallet.wallet?.walletAddress ?? '')); ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Address copied'))); }),
                ]),
              ),
              const SizedBox(height: 20),
              // Carbon Balance
              Center(child: Column(children: [
                const Text('Carbon Token Balance', style: TextStyle(fontSize: 14, color: AppColors.textMuted)),
                const SizedBox(height: 4),
                Text(fmt.format(wallet.totalBalance.toInt()), style: const TextStyle(fontSize: 36, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                const Text('tCO₂e Carbon Tokens', style: TextStyle(fontSize: 14, color: AppColors.textMuted)),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                  decoration: BoxDecoration(
                    color: AppColors.verifiedBg,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '≈ ${NumberFormat.currency(locale: 'id_ID', symbol: 'Rp ', decimalDigits: 0).format(wallet.totalBalance * 5000)}',
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.primary),
                  ),
                ),
              ])),
              const SizedBox(height: 20),
              // Action buttons
              Row(children: [
                Expanded(child: _WalletAction(icon: Icons.call_received, label: 'Receive', color: AppColors.primary, onTap: () => _showReceive(context, wallet.wallet?.walletAddress ?? ''))),
                const SizedBox(width: 12),
                Expanded(child: _WalletAction(icon: Icons.call_made, label: 'Send', color: AppColors.transfer, onTap: () => _showSend(context))),
                const SizedBox(width: 12),
                Expanded(child: _WalletAction(icon: Icons.swap_horiz, label: 'Swap', color: AppColors.secondary, onTap: () => _showComingSoon(context))),
              ]),
              const SizedBox(height: 24),
              // Transaction History
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                const Text('Transaction History', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                TextButton(onPressed: () {}, child: const Text('View All')),
              ]),
              const SizedBox(height: 8),
              ...wallet.transactions.map((tx) => BlockchainTxTile(tx: tx)),
            ]),
    );
  }

  void _showReceive(BuildContext context, String address) {
    showModalBottomSheet(context: context, builder: (_) => Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisSize: MainAxisSize.min, children: [
      Container(width: 40, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2))),
      const SizedBox(height: 20),
      const Icon(Icons.qr_code_2, size: 120, color: AppColors.primary),
      const SizedBox(height: 16),
      const Text('Your Wallet Address', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
      const SizedBox(height: 8),
      SelectableText(address, style: const TextStyle(fontFamily: 'monospace', fontSize: 12, color: AppColors.textSecondary)),
      const SizedBox(height: 16),
      SizedBox(width: double.infinity, child: ElevatedButton.icon(onPressed: () { Clipboard.setData(ClipboardData(text: address)); Navigator.pop(context); }, icon: const Icon(Icons.copy), label: const Text('Copy Address'))),
      const SizedBox(height: 8),
    ])));
  }

  void _showSend(BuildContext context) {
    showModalBottomSheet(context: context, isScrollControlled: true, builder: (_) => Padding(padding: EdgeInsets.only(left: 24, right: 24, top: 24, bottom: MediaQuery.of(context).viewInsets.bottom + 24), child: Column(mainAxisSize: MainAxisSize.min, children: [
      Container(width: 40, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2))),
      const SizedBox(height: 20),
      const Text('Send Tokens', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 16),
      const TextField(decoration: InputDecoration(labelText: 'Recipient Address', hintText: '0x...')),
      const SizedBox(height: 12),
      const TextField(decoration: InputDecoration(labelText: 'Amount (tCO₂e)'), keyboardType: TextInputType.number),
      const SizedBox(height: 16),
      SizedBox(width: double.infinity, child: ElevatedButton(onPressed: () {
        final hash = BlockchainService.generateTxHash(previousHash: BlockchainService.genesisHash, type: 'transfer', amount: 100, refId: 99, timestamp: DateTime.now().toIso8601String());
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Transfer sent: ${BlockchainService.truncateHash(hash)}'), backgroundColor: AppColors.primary));
      }, child: const Text('Send'))),
    ])));
  }

  void _showComingSoon(BuildContext ctx) {
    showDialog(context: ctx, builder: (_) => AlertDialog(title: const Text('Coming Soon'), content: const Text('Token swap feature is coming in a future update.'), actions: [TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK'))]));
  }
}

class _WalletAction extends StatelessWidget {
  final IconData icon; final String label; final Color color; final VoidCallback onTap;
  const _WalletAction({required this.icon, required this.label, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(onTap: onTap, child: Container(
      padding: const EdgeInsets.symmetric(vertical: 14),
      decoration: BoxDecoration(color: color.withValues(alpha: 0.08), borderRadius: BorderRadius.circular(12)),
      child: Column(mainAxisSize: MainAxisSize.min, children: [Icon(icon, color: color, size: 22), const SizedBox(height: 6), Text(label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: color))]),
    ));
  }
}
