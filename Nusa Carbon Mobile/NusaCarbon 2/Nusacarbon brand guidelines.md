# NusaCarbon Brand Guidelines — Flutter Mobile Edition

## Brand Name

**NusaCarbon**

"Nusa" means "island/archipelago" in Bahasa Indonesia — a direct reference to the Indonesian archipelago and its biodiversity. "Carbon" refers to carbon credits. Together: _Indonesian-origin, climate-focused, credible_.

### Acceptable Usage
- NusaCarbon (preferred — one word, capital N, capital C)
- NUSACARBON (all caps, splash screen / hero display only)
- nusacarbon (lowercase, URLs and technical contexts only)

### Unacceptable Usage
- Nusa Carbon (two words — never separate)
- nusaCarbon (camelCase — incorrect)
- Nusacarbon (lowercase C — incorrect)
- NusaC or NC (abbreviations — never in brand context)

---

## Brand Tagline

**Primary tagline:**
> "Transparent. Verified. Tokenized Carbon Credits."

**Short tagline (chips / limited space):**
> "Tokenized carbon. Verified impact."

### Tagline Rules
- Always use a period after each word in the three-part primary tagline
- Do not alter the word order (Transparent → Verified → Tokenized)
- Written in sentence case (not ALL CAPS)

---

## Mission Statement

NusaCarbon is Indonesia's blockchain-inspired carbon credit token marketplace, integrating dMRV (digital Monitoring, Reporting & Verification) to ensure every tokenized credit is real, measurable, and permanently recorded. We make climate action transparent and accessible.

---

## Logo

### Construction
1. **Icon mark:** Leaf symbol inside a rounded square with emerald-to-teal diagonal gradient
2. **Wordmark:** "NusaCarbon" in semi-bold sans-serif (use `FontWeight.w600`, system default or Google Fonts: Inter)

### Flutter Implementation

```dart
// Logo icon mark
Container(
  width: 36,
  height: 36,
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular(8),
    gradient: LinearGradient(
      colors: [Color(0xFF059669), Color(0xFF0F766E)],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    ),
  ),
  child: Icon(Icons.eco, color: Colors.white, size: 20),
  // Or use a custom leaf SVG asset
)

// Full logo (icon + wordmark)
Row(
  mainAxisSize: MainAxisSize.min,
  children: [
    // Icon mark above
    SizedBox(width: 8),
    Text(
      'NusaCarbon',
      style: TextStyle(
        fontWeight: FontWeight.w600,
        fontSize: 18,
        color: Color(0xFF047857), // Emerald 700 on light bg
        // Or Colors.white on dark bg
      ),
    ),
  ],
)
```

### Sizes
| Context | Icon Size | Total Width |
|---|---|---|
| AppBar (light) | 32×32px | ~130px |
| Splash screen | 56×56px | ~200px |
| Drawer header | 36×36px | ~140px |
| App icon (launcher) | See Flutter icon guide | 1024×1024px source |

### Logo Don'ts
- Do not stretch, rotate, or skew either element
- Do not change gradient direction or colors
- Do not add drop shadows to the icon mark
- Do not use icon alone except as app launcher icon
- Do not recolor wordmark in any color other than Emerald 700 or White

---

## Color Palette

### Primary Brand Colors

```dart
// lib/constants/app_colors.dart

class AppColors {
  // Primary brand color — emerald-700
  static const Color primary = Color(0xFF047857);

  // Active/button state — emerald-600
  static const Color primaryActive = Color(0xFF059669);

  // Hover/pressed state — emerald-800
  static const Color primaryDark = Color(0xFF065F46);

  // Secondary accent — teal-600
  static const Color secondary = Color(0xFF0D9488);

  // Deep teal — teal-700
  static const Color secondaryDark = Color(0xFF0F766E);

  // Page/scaffold background
  static const Color background = Color(0xFFF8FAFC); // slate-50

  // Card surface
  static const Color surface = Colors.white;

  // Dark background (drawer, bottom sheet header, dark cards)
  static const Color dark = Color(0xFF0F172A); // slate-900

  // Headings
  static const Color textPrimary = Color(0xFF0F172A); // slate-900

  // Body / labels
  static const Color textSecondary = Color(0xFF4B5563); // gray-600

  // Captions / metadata / placeholders
  static const Color textMuted = Color(0xFF94A3B8); // slate-400

  // Borders / dividers
  static const Color border = Color(0xFFE5E7EB); // gray-200

  // Status: Verified / Success
  static const Color verified = Color(0xFF059669);
  static const Color verifiedBg = Color(0xFFECFDF5); // emerald-50

  // Status: Pending / Warning
  static const Color pending = Color(0xFFF59E0B);
  static const Color pendingBg = Color(0xFFFFFBEB); // amber-50

  // Status: Rejected / Error
  static const Color rejected = Color(0xFFDC2626);
  static const Color rejectedBg = Color(0xFFFEF2F2); // red-50

  // Status: Transfer / Info
  static const Color transfer = Color(0xFF2563EB);
  static const Color transferBg = Color(0xFFEFF6FF); // blue-50

  // Gradient: hero section background
  static const LinearGradient heroGradient = LinearGradient(
    colors: [Color(0xFFECFDF5), Color(0xFFF0FDFA), Color(0xFFEFF6FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Gradient: primary button / metric card
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF059669), Color(0xFF0D9488)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Gradient: logo icon mark
  static const LinearGradient logoGradient = LinearGradient(
    colors: [Color(0xFF059669), Color(0xFF0F766E)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
```

### Project Type → Color Mapping (Flutter)
| Type | Background Color | Text Color |
|---|---|---|
| Forest | `Color(0xFFDCFCE7)` | `Color(0xFF166534)` |
| Mangrove | `Color(0xFFCCFBF1)` | `Color(0xFF115E59)` |
| Renewable Energy | `Color(0xFFDBEAFE)` | `Color(0xFF1E40AF)` |
| Blue Carbon | `Color(0xFFCFFAFE)` | `Color(0xFF155E75)` |
| Peatland | `Color(0xFFFEF3C7)` | `Color(0xFF92400E)` |

---

## Typography

### Font Stack
- Primary: Inter (import via `google_fonts` package: `GoogleFonts.inter()`)
- Fallback: System default (`TextStyle()` without explicit fontFamily)
- Monospace (hashes, token IDs, serial numbers): `fontFamily: 'monospace'` or `GoogleFonts.sourceCodePro()`

### Flutter ThemeData Typography

```dart
// lib/theme/app_theme.dart

ThemeData get appTheme => ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: AppColors.primary,
    primary: AppColors.primary,
    secondary: AppColors.secondary,
    surface: AppColors.surface,
    background: AppColors.background,
    error: AppColors.rejected,
  ),
  scaffoldBackgroundColor: AppColors.background,
  appBarTheme: AppBarTheme(
    backgroundColor: Colors.white,
    foregroundColor: AppColors.textPrimary,
    elevation: 0,
    shadowColor: Colors.transparent,
    surfaceTintColor: Colors.transparent,
    titleTextStyle: TextStyle(
      fontSize: 18,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),
  ),
  textTheme: TextTheme(
    // Hero headline
    displayLarge: TextStyle(
      fontSize: 32,
      fontWeight: FontWeight.bold,
      color: AppColors.textPrimary,
      letterSpacing: -0.5,
    ),
    // Screen titles
    headlineMedium: TextStyle(
      fontSize: 24,
      fontWeight: FontWeight.bold,
      color: AppColors.textPrimary,
    ),
    // Card titles
    titleLarge: TextStyle(
      fontSize: 18,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),
    titleMedium: TextStyle(
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),
    // Body text
    bodyLarge: TextStyle(fontSize: 16, color: AppColors.textSecondary),
    bodyMedium: TextStyle(fontSize: 14, color: AppColors.textSecondary),
    // Captions / metadata
    bodySmall: TextStyle(fontSize: 12, color: AppColors.textMuted),
    // Labels (badges, chips)
    labelLarge: TextStyle(fontSize: 13, fontWeight: FontWeight.w500),
    labelSmall: TextStyle(fontSize: 11, fontWeight: FontWeight.w500),
  ),
  cardTheme: CardThemeData(
    color: Colors.white,
    elevation: 2,
    shadowColor: Colors.black.withOpacity(0.08),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12), // rounded-xl
    ),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: AppColors.primary,
      foregroundColor: Colors.white,
      elevation: 0,
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8), // rounded-lg
      ),
      textStyle: TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
    ),
  ),
  outlinedButtonTheme: OutlinedButtonThemeData(
    style: OutlinedButton.styleFrom(
      foregroundColor: AppColors.primary,
      side: BorderSide(color: AppColors.primary),
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: AppColors.border),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: AppColors.border),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: AppColors.primary, width: 2),
    ),
    filled: true,
    fillColor: Colors.white,
    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
  ),
  chipTheme: ChipThemeData(
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(20), // rounded-full
    ),
    labelStyle: TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
    padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
  ),
  dividerTheme: DividerThemeData(
    color: AppColors.border,
    thickness: 1,
    space: 1,
  ),
  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    backgroundColor: Colors.white,
    selectedItemColor: AppColors.primary,
    unselectedItemColor: AppColors.textMuted,
    elevation: 8,
  ),
  tabBarTheme: TabBarThemeData(
    labelColor: AppColors.primary,
    unselectedLabelColor: AppColors.textMuted,
    indicatorColor: AppColors.primary,
    indicatorSize: TabBarIndicatorSize.tab,
  ),
  progressIndicatorTheme: ProgressIndicatorThemeData(
    color: AppColors.primary,
    linearTrackColor: AppColors.border,
  ),
);
```

---

## Component Specifications

### Border Radius Standards
| Component | Flutter `BorderRadius` | px |
|---|---|---|
| Buttons, inputs, chips | `BorderRadius.circular(8)` | 8px |
| Cards, panels | `BorderRadius.circular(12)` | 12px |
| Hero cards, image containers | `BorderRadius.circular(16)` | 16px |
| Circular badges | `BorderRadius.circular(20)` | 20px |
| App icon, logo container | `BorderRadius.circular(8)` | 8px |

### Spacing System
Use multiples of 4px for all padding/margin:
- `4` (tight) · `8` (small) · `12` (compact) · `16` (standard) · `20/24` (medium) · `32` (section) · `48/64` (large)

### Elevation / Shadow
```dart
// Card shadow (standard)
BoxShadow(
  color: Colors.black.withOpacity(0.06),
  blurRadius: 12,
  offset: Offset(0, 4),
)

// Card shadow (hover / elevated)
BoxShadow(
  color: Colors.black.withOpacity(0.12),
  blurRadius: 24,
  offset: Offset(0, 8),
)
```

### Metric Card (Gradient)
```dart
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    gradient: AppColors.primaryGradient, // or custom per card
    borderRadius: BorderRadius.circular(12),
  ),
  child: Column(/* metric value + label */),
)
```

### Status Badges / Chips
```dart
// Verified badge
Container(
  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  decoration: BoxDecoration(
    color: AppColors.verifiedBg,
    borderRadius: BorderRadius.circular(20),
  ),
  child: Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Icon(Icons.check_circle, color: AppColors.verified, size: 14),
      SizedBox(width: 4),
      Text('Verified', style: TextStyle(color: AppColors.verified, fontSize: 12, fontWeight: FontWeight.w600)),
    ],
  ),
)
```

### Token ID / Hash Display
```dart
// Monospace, muted color, truncated
Text(
  '0x7a8f...1b0c',
  style: TextStyle(
    fontFamily: 'monospace',
    fontSize: 12,
    color: AppColors.textMuted,
    letterSpacing: 0.5,
  ),
)
```

---

## Icons

### Primary Icon Library
Use Flutter's built-in `Icons` (Material) as the default.

| Concept | Material Icon |
|---|---|
| Logo / brand | `Icons.eco` (leaf) |
| Location | `Icons.location_on` |
| Calendar / date | `Icons.calendar_today` |
| Blockchain / shield | `Icons.shield` |
| Verified | `Icons.check_circle` |
| Pending | `Icons.hourglass_empty` |
| Rejected | `Icons.cancel` |
| Mint (create) | `Icons.add_circle_outline` |
| Transfer (buy) | `Icons.swap_horiz` |
| Retire (burn) | `Icons.local_fire_department` |
| Chart / analytics | `Icons.bar_chart` |
| Portfolio | `Icons.account_balance_wallet` |
| Settings | `Icons.settings` |
| Notifications | `Icons.notifications_outlined` |
| Copy | `Icons.copy_all` |
| External link | `Icons.open_in_new` |

---

## Animation Guidelines

### Flutter Animation Approach
Use `AnimationController` + `FadeTransition` / `SlideTransition` for page-level animations.
For simple cases, use `AnimatedOpacity` and `AnimatedContainer`.

```dart
// Fade-up entry animation pattern (use on screen initState)
class FadeUpAnimation extends StatefulWidget {
  final Widget child;
  final Duration delay;
  // ... implement AnimationController with FadeTransition + SlideTransition
}
```

### Timing Standards
| Animation | Duration | Curve |
|---|---|---|
| Screen entry | 400ms | `Curves.easeOut` |
| Card appear (staggered) | 300ms (50ms delay between items) | `Curves.easeOut` |
| Button press feedback | 100ms | `Curves.easeIn` |
| Bottom sheet slide | 300ms | `Curves.easeOutCubic` |
| Loading shimmer | 1200ms loop | `Curves.linear` |

---

## Charts (fl_chart)

### Line Chart (dMRV Data)
```dart
LineChartData(
  gridData: FlGridData(
    drawVerticalLine: false,
    getDrawingHorizontalLine: (_) => FlLine(
      color: AppColors.border,
      strokeWidth: 1,
    ),
  ),
  titlesData: FlTitlesData(/* quarters on x-axis */),
  borderData: FlBorderData(show: false),
  lineBarsData: [
    LineChartBarData(
      isCurved: true,
      color: AppColors.primary,
      barWidth: 2.5,
      belowBarData: BarAreaData(
        show: true,
        color: AppColors.primary.withOpacity(0.08),
      ),
    ),
  ],
)
```

### Pie Chart (Portfolio Breakdown)
```dart
// Slice colors — use this order:
const List<Color> pieColors = [
  Color(0xFF059669), // emerald-600
  Color(0xFF0D9488), // teal-600
  Color(0xFF2563EB), // blue-600
  Color(0xFF7C3AED), // violet-600
  Color(0xFFF59E0B), // amber-500
  Color(0xFFEC4899), // pink-500
];
```

### Bar Chart (Revenue)
```dart
// Bar color: primaryGradient (emerald → teal)
// Axis labels: months abbreviated (Jan, Feb, Mar...)
// Y-axis: USD formatted ($X,XXX)
```

---

## Image Guidelines

### CachedNetworkImage with Gradient Fallback
```dart
ClipRRect(
  borderRadius: BorderRadius.circular(12),
  child: CachedNetworkImage(
    imageUrl: project.imageUrl,
    height: 120, // token card
    width: double.infinity,
    fit: BoxFit.cover,
    placeholder: (_, __) => Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFFD1FAE5), Color(0xFFCCFBF1)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
    ),
    errorWidget: (_, __, ___) => Container(
      color: Color(0xFFECFDF5),
      child: Icon(Icons.eco, color: AppColors.primary, size: 40),
    ),
  ),
)
```

### Image Heights by Context
| Context | Height |
|---|---|
| TokenCard image | 120px |
| ProjectDetailScreen hero | 220px |
| Splash screen background (if used) | full screen |

---

## Writing Style

### Brand Voice Pillars

**Credible** — Reference verification standards by name (Verra, Gold Standard, Plan Vivo).
**Transparent** — Explain how things work: what dMRV means, how tokens are minted.
**Accessible** — Climate finance is complex; make it understandable without being patronizing.
**Indonesian-proud** — Celebrate Indonesia's biodiversity. Specific is better than generic.

### Key Vocabulary

**Use consistently:**
- Carbon credit token (not "carbon coin" or "eco-token")
- tCO₂e (tonnes of CO₂ equivalent) — always include the "e"
- dMRV (spell out on first use per screen: "digital Monitoring, Reporting & Verification")
- Retire / retirement (when claiming offsets) — not "burn," "destroy," "use"
- Mint / minting (when creating tokens) — not "issue," "create"
- Vintage year — not "batch year"
- Verified — not "approved" or "certified" (in marketplace context)

### Number Formatting (Dart)

```dart
// Token quantities — use intl package
final formatter = NumberFormat('#,###');
formatter.format(125000); // → "125,000"

// USD prices
NumberFormat.currency(symbol: '\$', decimalDigits: 0).format(15); // → "$15"
NumberFormat.currency(symbol: '\$').format(1680000); // → "$1,680,000"

// Percentages — no space before %
'${score.toStringAsFixed(0)}%' // → "96%"

// Dates — ISO in data, human-readable in UI
DateFormat('MMM d, yyyy').format(date); // → "Dec 10, 2025"
DateFormat('Q\'Q\' yyyy').format(date); // → "Q1 2025" (quarters)
```

---

## Accessibility

- All images: use `semanticLabel` parameter in `CachedNetworkImage` / `Image`
- Icon-only buttons: wrap with `Tooltip` widget
- Status chips: use text + icon (never color alone to indicate status)
- Minimum touch target: 48×48dp (per Material guidelines)
- Text contrast: maintain WCAG AA minimum 4.5:1 ratio
  - Emerald-700 (#047857) on white: ✅ 7.1:1
  - White on Emerald-600 (#059669): ✅ 4.6:1

---

## Token ID & Naming Conventions

```
Token ID:      TKN-{CODE}-{NUM}-B{BATCH}    e.g. TKN-LSR-001-B1
Serial Range:  NC-{CODE}-{NUM}-{START} to NC-{CODE}-{NUM}-{END}
               e.g. NC-LSR-001-000001 to NC-LSR-001-450000
Tx Hash:       0x{full-sha256}              displayed as 0x7a8f...1b0c
Cert ID:       CERT-{RET_NUM}-{YEAR}        e.g. CERT-001-2025
```

| Code | Project |
|---|---|
| LSR | Leuser Ecosystem Forest Conservation |
| PPM | Papua Mangrove Restoration |
| JSF | Java Solar Farm Initiative |
| KPR | Kalimantan Peatland Restoration |
| SBC | Sulawesi Blue Carbon Initiative |
| SAF | Sumatra Agroforestry Program |

---

## Copyright

`© 2026 NusaCarbon. All rights reserved.`

Displayed in app: About screen footer, splash screen bottom text.
