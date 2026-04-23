import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'theme/app_theme.dart';
import 'router.dart';
import 'providers/auth_provider.dart';
import 'providers/home_provider.dart';
import 'providers/tokens_provider.dart';
import 'providers/wallet_provider.dart';
import 'providers/marketplace_provider.dart';
import 'providers/owner_provider.dart';
import 'providers/verifier_provider.dart';
import 'providers/account_provider.dart';
import 'providers/admin_provider.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const NusaCarbonApp());
}

class NusaCarbonApp extends StatelessWidget {
  const NusaCarbonApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()..init()),
        ChangeNotifierProvider(create: (_) => AccountProvider()..init()),
        ChangeNotifierProvider(create: (_) => HomeProvider()),
        ChangeNotifierProvider(create: (_) => TokensProvider()),
        ChangeNotifierProvider(create: (_) => WalletProvider()),
        ChangeNotifierProvider(create: (_) => MarketplaceProvider()),
        ChangeNotifierProvider(create: (_) => OwnerProvider()),
        ChangeNotifierProvider(create: (_) => VerifierProvider()),
        ChangeNotifierProvider(create: (_) => AdminProvider()),
      ],
      child: Consumer<AuthProvider>(
        builder: (context, authProvider, _) {
          final router = createRouter(authProvider);
          return MaterialApp.router(
            title: 'NusaCarbon',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.appTheme,
            routerConfig: router,
          );
        },
      ),
    );
  }
}
