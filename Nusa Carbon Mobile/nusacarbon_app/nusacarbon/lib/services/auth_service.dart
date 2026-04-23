import 'package:shared_preferences/shared_preferences.dart';

/// Authentication and role management service.
///
/// Stores user role in SharedPreferences.
/// Roles: buyer, project_owner, verifier, admin
class AuthService {
  AuthService._();

  static const String _roleKey = 'user_role';

  /// Save user role to SharedPreferences
  static Future<void> saveRole(String role) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_roleKey, role);
  }

  /// Get the current user role (null if not set → redirect to splash)
  static Future<String?> getRole() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_roleKey);
  }

  /// Clear user role (logout) — removes all stored data
  static Future<void> clearRole() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_roleKey);
  }

  /// Check if a user role is stored
  static Future<bool> isLoggedIn() async {
    final role = await getRole();
    return role != null && role.isNotEmpty;
  }
}
