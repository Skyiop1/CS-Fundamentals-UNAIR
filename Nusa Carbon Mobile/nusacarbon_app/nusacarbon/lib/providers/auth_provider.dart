import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import '../models/user_model.dart';
import '../providers/account_provider.dart';

/// Manages the current session: selected role, loaded user, loading state.
///
/// Real user data is fetched from [ApiService] on [init] and [selectRole].
/// No mock data is used when [ApiService.useMock] is false.
class AuthProvider extends ChangeNotifier {
  String? _role;
  UserModel? _user;
  bool _isLoading = true;
  String? _error;

  String? get role => _role;
  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  bool get isLoggedIn => _role != null;
  String? get error => _error;

  // ─── Init ────────────────────────────────────────────────────────────

  /// Called once at app start. Restores any persisted role and loads the
  /// matching user from the API.
  Future<void> init() async {
    _isLoading = true;
    notifyListeners();

    _role = await AuthService.getRole();
    if (_role != null) {
      await _loadUserForRole(_role!);
    }

    _isLoading = false;
    notifyListeners();
  }

  // ─── Role Selection ──────────────────────────────────────────────────

  /// Persists [role], fetches the matching user from the API, and optionally
  /// syncs [accountProvider] so [AccountProvider.currentUserId] is immediately
  /// correct without waiting for a hot restart.
  Future<void> selectRole(
    String role, {
    AccountProvider? accountProvider,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    await AuthService.saveRole(role);
    _role = role;

    // Keep AccountProvider in sync right away (no restart needed).
    accountProvider?.setAuthRole(role);

    await _loadUserForRole(role);

    _isLoading = false;
    notifyListeners();
  }

  // ─── Logout ──────────────────────────────────────────────────────────

  Future<void> logout({AccountProvider? accountProvider}) async {
    await AuthService.clearRole();
    _role = null;
    _user = null;
    _error = null;
    accountProvider?.setAuthRole(null);
    notifyListeners();
  }

  // ─── Private helpers ─────────────────────────────────────────────────

  /// Maps a role string to the matching seeded database user ID and loads
  /// that user from the API. Falls back to a minimal offline stub only when
  /// the API call fails so the UI never gets a null user.
  Future<void> _loadUserForRole(String role) async {
    final userId = _roleToUserId(role);
    try {
      final api = ApiService();
      final res = await api.getUserById(userId);
      if (res.statusCode == 200) {
        final data = res.data['data'];
        if (data != null) {
          _user = UserModel.fromJson(data as Map<String, dynamic>);
          return;
        }
      }
      // Non-200 response: fall through to offline stub
      _user = _offlineStub(role, userId);
    } catch (e) {
      debugPrint('AuthProvider: could not load user ($e) — using offline stub');
      _user = _offlineStub(role, userId);
    }
  }

  /// Role → seeded user ID mapping. Must stay in sync with DataSeeder.
  int _roleToUserId(String role) {
    switch (role) {
      case 'project_owner':
        return 2;
      case 'verifier':
        return 3;
      case 'admin':
        return 4;
      case 'buyer':
      case 'investor':
      default:
        return 1;
    }
  }

  /// Minimal offline stub used when the API is unreachable.
  /// Ensures [user] is never null so the UI can always render.
  UserModel _offlineStub(String role, int userId) {
    const names = {
      1: 'PT Carbon Indonesia',
      2: 'PT Hijau Nusantara',
      3: 'Badan Verifikasi Nasional',
      4: 'Admin NusaCarbon',
    };
    const emails = {
      1: 'carbonpt@nusacarbon.co.id',
      2: 'owner@nusacarbon.co.id',
      3: 'verifier@nusacarbon.co.id',
      4: 'admin@nusacarbon.co.id',
    };
    return UserModel(
      idUser: userId,
      namaUser: names[userId] ?? 'NusaCarbon User',
      email: emails[userId] ?? 'user@nusacarbon.co.id',
      statusKyc: 'verified',
      roleName: role,
      createdAt: DateTime(2024, 1, 15),
    );
  }
}
