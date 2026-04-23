import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'providers/auth_provider.dart';
import 'screens/splash_screen.dart';
import 'screens/home_screen.dart';
import 'screens/tokens_screen.dart';
import 'screens/token_detail_screen.dart';
import 'screens/wallet_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/marketplace_screen.dart';
import 'screens/project_detail_screen.dart';
import 'screens/verifier_dashboard_screen.dart';
import 'screens/owner_dashboard_screen.dart';
import 'screens/admin_screen.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

GoRouter createRouter(AuthProvider authProvider) {
  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: '/splash',
    redirect: (context, state) {
      final isLoggedIn = authProvider.isLoggedIn;
      final isOnSplash = state.matchedLocation == '/splash';
      if (!isLoggedIn && !isOnSplash) return '/splash';
      if (isLoggedIn && isOnSplash) return '/home';
      return null;
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      // Shell route with bottom navigation
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) => MainShell(child: child),
        routes: [
          GoRoute(path: '/home', builder: (_, __) => const HomeScreen()),
          GoRoute(path: '/tokens', builder: (_, __) => const TokensScreen()),
          GoRoute(path: '/wallet', builder: (_, __) => const WalletScreen()),
          GoRoute(path: '/profile', builder: (_, __) => const ProfileScreen()),
        ],
      ),
      // Full-screen routes (outside shell)
      GoRoute(path: '/tokens/:tokenId', builder: (_, state) => TokenDetailScreen(tokenId: int.parse(state.pathParameters['tokenId']!))),
      GoRoute(path: '/marketplace', builder: (_, __) => const MarketplaceScreen()),
      GoRoute(path: '/project/:projectId', builder: (_, state) => ProjectDetailScreen(projectId: int.parse(state.pathParameters['projectId']!))),
      GoRoute(path: '/dashboard/verifier', builder: (_, __) => const VerifierDashboardScreen()),
      GoRoute(path: '/dashboard/owner', builder: (_, __) => const OwnerDashboardScreen()),
      GoRoute(path: '/admin', builder: (_, __) => const AdminScreen()),
    ],
  );
}

class MainShell extends StatelessWidget {
  final Widget child;
  const MainShell({super.key, required this.child});

  static int _indexOf(String location) {
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/tokens')) return 1;
    if (location.startsWith('/wallet')) return 2;
    if (location.startsWith('/profile')) return 3;
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    final currentIndex = _indexOf(location);

    return Scaffold(
      body: child,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: (index) {
          switch (index) {
            case 0: context.go('/home'); break;
            case 1: context.go('/tokens'); break;
            case 2: context.go('/wallet'); break;
            case 3: context.go('/profile'); break;
          }
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'Tokens'),
          BottomNavigationBarItem(icon: Icon(Icons.account_balance_wallet), label: 'Wallet'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
