import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  // ─── Primary Brand Colors ─────────────────────────────────────────────
  /// Primary brand color — emerald-700
  static const Color primary = Color(0xFF047857);

  /// Active/button state — emerald-600
  static const Color primaryActive = Color(0xFF059669);

  /// Hover/pressed state — emerald-800
  static const Color primaryDark = Color(0xFF065F46);

  /// Secondary accent — teal-600
  static const Color secondary = Color(0xFF0D9488);

  /// Deep teal — teal-700
  static const Color secondaryDark = Color(0xFF0F766E);

  // ─── Background & Surface ─────────────────────────────────────────────
  /// Page/scaffold background — slate-50
  static const Color background = Color(0xFFF8FAFC);

  /// Card surface
  static const Color surface = Colors.white;

  /// Dark background (drawer, bottom sheet header, dark cards) — slate-900
  static const Color dark = Color(0xFF0F172A);

  // ─── Text Colors ──────────────────────────────────────────────────────
  /// Headings — slate-900
  static const Color textPrimary = Color(0xFF0F172A);

  /// Body / labels — gray-600
  static const Color textSecondary = Color(0xFF4B5563);

  /// Captions / metadata / placeholders — slate-400
  static const Color textMuted = Color(0xFF94A3B8);

  // ─── Borders ──────────────────────────────────────────────────────────
  /// Borders / dividers — gray-200
  static const Color border = Color(0xFFE5E7EB);

  // ─── Status Colors ────────────────────────────────────────────────────
  /// Status: Verified / Success
  static const Color verified = Color(0xFF059669);
  static const Color verifiedBg = Color(0xFFECFDF5);

  /// Status: Pending / Warning
  static const Color pending = Color(0xFFF59E0B);
  static const Color pendingBg = Color(0xFFFFFBEB);

  /// Status: Rejected / Error
  static const Color rejected = Color(0xFFDC2626);
  static const Color rejectedBg = Color(0xFFFEF2F2);

  /// Status: Transfer / Info
  static const Color transfer = Color(0xFF2563EB);
  static const Color transferBg = Color(0xFFEFF6FF);

  // ─── Gradients ────────────────────────────────────────────────────────
  /// Gradient: hero section background
  static const LinearGradient heroGradient = LinearGradient(
    colors: [Color(0xFFECFDF5), Color(0xFFF0FDFA), Color(0xFFEFF6FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  /// Gradient: primary button / metric card / portfolio hero
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF059669), Color(0xFF0D9488)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  /// Gradient: logo icon mark
  static const LinearGradient logoGradient = LinearGradient(
    colors: [Color(0xFF059669), Color(0xFF0F766E)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ─── Project Type Colors ──────────────────────────────────────────────
  static const Color forestBg = Color(0xFFDCFCE7);
  static const Color forestText = Color(0xFF166534);

  static const Color mangroveBg = Color(0xFFCCFBF1);
  static const Color mangroveText = Color(0xFF115E59);

  static const Color renewableBg = Color(0xFFDBEAFE);
  static const Color renewableText = Color(0xFF1E40AF);

  static const Color blueCarbonBg = Color(0xFFCFFAFE);
  static const Color blueCarbonText = Color(0xFF155E75);

  static const Color peatlandBg = Color(0xFFFEF3C7);
  static const Color peatlandText = Color(0xFF92400E);

  /// Get project type colors by category name
  static ({Color bg, Color text}) projectTypeColors(String category) {
    switch (category.toLowerCase()) {
      case 'hutan':
      case 'forest':
        return (bg: forestBg, text: forestText);
      case 'mangrove':
        return (bg: mangroveBg, text: mangroveText);
      case 'energi terbarukan':
      case 'renewable energy':
        return (bg: renewableBg, text: renewableText);
      case 'blue carbon':
        return (bg: blueCarbonBg, text: blueCarbonText);
      case 'lahan gambut':
      case 'peatland':
        return (bg: peatlandBg, text: peatlandText);
      default:
        return (bg: verifiedBg, text: primary);
    }
  }

  // ─── Pie Chart Colors ─────────────────────────────────────────────────
  static const List<Color> pieColors = [
    Color(0xFF059669), // emerald-600
    Color(0xFF0D9488), // teal-600
    Color(0xFF2563EB), // blue-600
    Color(0xFF7C3AED), // violet-600
    Color(0xFFF59E0B), // amber-500
    Color(0xFFEC4899), // pink-500
  ];

  // ─── Indigo (Verifier role) ───────────────────────────────────────────
  static const Color indigo = Color(0xFF4F46E5);
  static const Color indigoBg = Color(0xFFEEF2FF);
}
