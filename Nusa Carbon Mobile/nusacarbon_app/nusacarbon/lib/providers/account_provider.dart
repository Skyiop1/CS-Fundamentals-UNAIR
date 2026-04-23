import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum AccountMode { investor, developer }

class AccountProvider extends ChangeNotifier {
  static const String _modeKey = 'account_mode_key';

  // Shared-preferences key written by AuthService
  static const String _roleKey = 'user_role';

  AccountMode _currentMode = AccountMode.investor;
  String? _authRole;
  bool _isLoading = true;

  AccountMode get currentMode => _currentMode;
  bool get isLoading => _isLoading;
  bool get isInvestor => _currentMode == AccountMode.investor;
  bool get isDeveloper => _currentMode == AccountMode.developer;

  /// Returns the database user-ID that matches the currently selected role.
  ///
  /// For verifier / admin roles the ID is fixed by role.
  /// For buyer / project_owner roles the investor↔developer mode toggle
  /// controls whether we act as the buyer (1) or the owner (2).
  int get currentUserId {
    switch (_authRole) {
      case 'verifier':
        return 3;
      case 'admin':
        return 4;
      case 'project_owner':
        // project_owner always maps to owner user, regardless of mode
        return 2;
      case 'buyer':
      case 'investor':
      default:
        // Buyer can toggle between investor view (1) and developer view (2)
        return isInvestor ? 1 : 2;
    }
  }

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();

    // Read persisted mode toggle
    final modeString = prefs.getString(_modeKey);
    if (modeString == AccountMode.developer.name) {
      _currentMode = AccountMode.developer;
    } else {
      _currentMode = AccountMode.investor;
    }

    // Read the role saved by AuthService so currentUserId is correct
    _authRole = prefs.getString(_roleKey);

    _isLoading = false;
    notifyListeners();
  }

  /// Called from [AuthProvider.selectRole] so the provider stays in sync
  /// without requiring a full restart.
  void setAuthRole(String? role) {
    _authRole = role;
    notifyListeners();
  }

  Future<void> toggleMode() async {
    _currentMode =
        _currentMode == AccountMode.investor
            ? AccountMode.developer
            : AccountMode.investor;

    notifyListeners();

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_modeKey, _currentMode.name);
  }
}
