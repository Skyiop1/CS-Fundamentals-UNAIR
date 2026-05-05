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

import 'package:provider/provider.dart';
import 'providers/account_provider.dart';

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
      
      if (isLoggedIn && isOnSplash) {
        // Redirect based on role
        final role = authProvider.role ?? 'buyer';
        if (role == 'admin') return '/admin';
        if (role == 'project_owner') return '/dashboard/owner';
        if (role == 'verifier') return '/dashboard/verifier';
        return '/home'; // Default for buyer/investor
      }
      return null;
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      
      // Shell route with dynamic bottom navigation
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) => MainShell(child: child),
        routes: [
          // Buyer Routes
          GoRoute(path: '/home', builder: (_, __) => const HomeScreen()),
          GoRoute(path: '/tokens', builder: (_, __) => const TokensScreen()),
          GoRoute(path: '/wallet', builder: (_, __) => const WalletScreen()),
          
          // Shared Marketplace (inside shell for Project Owner tab)
          GoRoute(path: '/marketplace', builder: (_, __) => const MarketplaceScreen()),
          
          // Project Owner Routes
          GoRoute(path: '/dashboard/owner', builder: (_, __) => const OwnerDashboardScreen()),
          
          // Verifier Routes
          GoRoute(path: '/dashboard/verifier', builder: (_, __) => const VerifierDashboardScreen()),
          
          // Admin Routes
          GoRoute(path: '/admin', builder: (_, __) => const AdminScreen()),

          // Shared Profile Route
          GoRoute(path: '/profile', builder: (_, __) => const ProfileScreen()),
        ],
      ),
      
      // Full-screen routes (outside shell)
      GoRoute(path: '/tokens/:tokenId', builder: (_, state) => TokenDetailScreen(tokenId: int.parse(state.pathParameters['tokenId']!))),
      GoRoute(path: '/project/:projectId', builder: (_, state) => ProjectDetailScreen(projectId: int.parse(state.pathParameters['projectId']!))),
    ],
  );
}

class MainShell extends StatelessWidget {
  final Widget child;
  const MainShell({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    final account = context.watch<AccountProvider>();
    final role = account.currentMode == AccountMode.developer ? 'project_owner' : context.read<AuthProvider>().role ?? 'buyer';

    List<BottomNavigationBarItem> items = [];
    List<String> routes = [];

    if (role == 'admin') {
      items = const [
        BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: 'Dashboard'),
        BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
      ];
      routes = ['/admin', '/profile'];
    } else if (role == 'project_owner') {
      items = const [
        BottomNavigationBarItem(icon: Icon(Icons.business_center), label: 'Dashboard'),
        BottomNavigationBarItem(icon: Icon(Icons.store), label: 'Marketplace'),
        BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
      ];
      routes = ['/dashboard/owner', '/marketplace', '/profile'];
    } else if (role == 'verifier') {
      items = const [
        BottomNavigationBarItem(icon: Icon(Icons.verified_user), label: 'Tasks'),
        BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
      ];
      routes = ['/dashboard/verifier', '/profile'];
    } else {
      // Default: Buyer
      items = const [
        BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
        BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'Tokens'),
        BottomNavigationBarItem(icon: Icon(Icons.account_balance_wallet), label: 'Wallet'),
        BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
      ];
      routes = ['/home', '/tokens', '/wallet', '/profile'];
    }

    // Determine current index based on location and available routes
    int currentIndex = routes.indexWhere((r) => location.startsWith(r));
    if (currentIndex == -1) currentIndex = 0; // Fallback

    // Special case for marketplace when in owner mode, we need a way to navigate to marketplace but keep the shell. Wait, marketplace is defined OUTSIDE shell.
    // If we want marketplace IN shell for owner, we must change route config.
    // Actually, since marketplace is outside shell, navigating there will hide bottom nav. Let's just use it as is, or we can make a dummy tab.

    return Scaffold(
      body: child,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        type: BottomNavigationBarType.fixed, // To show labels and multiple items correctly
        onTap: (index) {
          if (index < routes.length) {
            context.go(routes[index]);
          }
        },
        items: items,
      ),
    );
  }
}
