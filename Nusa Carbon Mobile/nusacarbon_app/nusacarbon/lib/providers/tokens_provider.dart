import 'package:flutter/material.dart';
import '../models/carbon_token.dart';
import '../services/api_service.dart';

/// A grouped view of tokens per project.
class TokenProjectGroup {
  final int idProject;
  final String namaProject;
  final String lokasi;
  final String namaKategori;
  final String? imageUrl;
  final int vintageYear;
  final int totalTokens;
  final int availableCount;
  final int listedCount;
  final int soldCount;
  final int retiredCount;
  final String? txMintHash; // first token's hash for display
  final DateTime createdAt;

  /// Dominant status for display purposes
  String get dominantStatus {
    if (availableCount > 0) return 'available';
    if (listedCount > 0) return 'listed';
    if (soldCount > 0) return 'sold';
    if (retiredCount > 0) return 'retired';
    return 'available';
  }

  const TokenProjectGroup({
    required this.idProject,
    required this.namaProject,
    required this.lokasi,
    required this.namaKategori,
    this.imageUrl,
    required this.vintageYear,
    required this.totalTokens,
    required this.availableCount,
    required this.listedCount,
    required this.soldCount,
    required this.retiredCount,
    this.txMintHash,
    required this.createdAt,
  });
}

class TokensProvider extends ChangeNotifier {
  List<CarbonToken> _allTokens = [];
  String _searchQuery = '';
  String _activeTab = 'All';
  bool _isLoading = false;
  String? _error;

  // ─── Grouped tokens by project ──────────────────────────────────
  List<TokenProjectGroup> get _groupedTokens {
    final Map<int, List<CarbonToken>> groups = {};
    for (final token in _allTokens) {
      groups.putIfAbsent(token.idProject, () => []).add(token);
    }

    return groups.entries.map((entry) {
      final tokens = entry.value;
      final first = tokens.first;
      return TokenProjectGroup(
        idProject: entry.key,
        namaProject: first.namaProject,
        lokasi: first.lokasi,
        namaKategori: first.namaKategori,
        imageUrl: first.imageUrl,
        vintageYear: first.vintageYear,
        totalTokens: tokens.length,
        availableCount: tokens.where((t) => t.statusToken == 'available').length,
        listedCount: tokens.where((t) => t.statusToken == 'listed').length,
        soldCount: tokens.where((t) => t.statusToken == 'sold').length,
        retiredCount: tokens.where((t) => t.statusToken == 'retired').length,
        txMintHash: first.txMintHash,
        createdAt: first.createdAt,
      );
    }).toList()
      ..sort((a, b) => b.totalTokens.compareTo(a.totalTokens));
  }

  List<TokenProjectGroup> get filteredGroups {
    var groups = _groupedTokens;

    // Tab filter
    switch (_activeTab) {
      case 'Available':
        groups = groups.where((g) => g.availableCount > 0).toList();
        break;
      case 'Retired':
        groups = groups.where((g) => g.retiredCount > 0).toList();
        break;
      case 'Listed':
        groups = groups.where((g) => g.listedCount > 0).toList();
        break;
    }

    // Search filter
    if (_searchQuery.isNotEmpty) {
      final q = _searchQuery.toLowerCase();
      groups = groups
          .where((g) =>
              g.namaProject.toLowerCase().contains(q) ||
              g.lokasi.toLowerCase().contains(q) ||
              g.namaKategori.toLowerCase().contains(q))
          .toList();
    }

    return groups;
  }

  String get activeTab => _activeTab;
  bool get isLoading => _isLoading;
  String? get error => _error;

  int get totalTokenCount => _allTokens.length;
  int get activeProjectCount =>
      _allTokens.map((t) => t.idProject).toSet().length;
  int get availableTokenCount =>
      _allTokens.where((t) => t.statusToken == 'available').length;
  int get listedTokenCount =>
      _allTokens.where((t) => t.statusToken == 'listed').length;

  Future<void> loadTokens(int userId, {bool isDeveloper = false}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final api = ApiService();
      final res = await api.getTokens(ownerId: userId);
      if (res.statusCode == 200) {
        final resData = res.data['data'] as List?;
        if (resData != null) {
          _allTokens = resData.map((t) => CarbonToken.fromJson(t)).toList();
        }
      } else {
        _error = 'Server returned ${res.statusCode}';
      }
    } catch (e) {
      _error = e.toString();
      debugPrint('Error loading tokens: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void setTab(String tab) {
    _activeTab = tab;
    notifyListeners();
  }

  void setSearch(String query) {
    _searchQuery = query;
    notifyListeners();
  }
}
