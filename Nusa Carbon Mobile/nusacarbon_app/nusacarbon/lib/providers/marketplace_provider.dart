import 'package:flutter/material.dart';
import '../models/carbon_project.dart';
import '../services/api_service.dart';

/// Manages marketplace projects — shows active/verified projects with
/// descriptions, categories, and details.
///
/// Category filter → passed as ?kategori= query param to GET /api/projects
/// Search & sort   → applied client-side on the already-filtered result set
class MarketplaceProvider extends ChangeNotifier {
  List<CarbonProject> _projects = [];
  String _searchQuery = '';
  String? _categoryFilter;
  String _sortBy = 'newest';
  bool _isLoading = false;
  String? _error;

  // ─── Getters ────────────────────────────────────────────────────────────

  bool get isLoading => _isLoading;
  String? get categoryFilter => _categoryFilter;
  String get sortBy => _sortBy;
  String? get error => _error;

  /// Returns the server-filtered list with search and sort applied on top.
  List<CarbonProject> get filteredProjects {
    var list = List<CarbonProject>.from(_projects);

    // Client-side search
    if (_searchQuery.isNotEmpty) {
      final q = _searchQuery.toLowerCase();
      list =
          list
              .where(
                (p) =>
                    p.namaProject.toLowerCase().contains(q) ||
                    p.lokasi.toLowerCase().contains(q) ||
                    p.namaKategori.toLowerCase().contains(q) ||
                    (p.deskripsi?.toLowerCase().contains(q) ?? false) ||
                    (p.ownerName?.toLowerCase().contains(q) ?? false),
              )
              .toList();
    }

    // Client-side sort
    switch (_sortBy) {
      case 'name_az':
        list.sort(
          (a, b) => a.namaProject.compareTo(b.namaProject),
        );
        break;
      case 'name_za':
        list.sort(
          (a, b) => b.namaProject.compareTo(a.namaProject),
        );
        break;
      case 'area_large':
        list.sort((a, b) => b.luasLahan.compareTo(a.luasLahan));
        break;
      case 'area_small':
        list.sort((a, b) => a.luasLahan.compareTo(b.luasLahan));
        break;
      case 'newest':
      default:
        list.sort((a, b) => b.createdAt.compareTo(a.createdAt));
        break;
    }

    return list;
  }

  // ─── Load ────────────────────────────────────────────────────────────────

  /// Fetches active/verified projects from the API.
  Future<void> loadProjects() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final api = ApiService();
      final res = await api.getProjects(
        status: 'verified',
        kategori: _categoryFilter,
      );

      if (res.statusCode == 200) {
        final raw = res.data['data'] as List?;
        if (raw != null) {
          _projects =
              raw
                  .map(
                    (p) =>
                        CarbonProject.fromJson(p as Map<String, dynamic>),
                  )
                  .toList();
        }
      } else {
        _error = 'Server returned ${res.statusCode}';
      }
    } catch (e) {
      _error = e.toString();
      debugPrint('MarketplaceProvider.loadProjects error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // ─── Filter / Sort controls ──────────────────────────────────────────────

  /// Sets the category filter and immediately reloads from the API.
  void setCategory(String? cat) {
    if (_categoryFilter == cat) return;
    _categoryFilter = cat;
    loadProjects();
  }

  void setSortBy(String sort) {
    _sortBy = sort;
    notifyListeners();
  }

  void setSearch(String q) {
    _searchQuery = q;
    notifyListeners();
  }

  void clearFilters() {
    _categoryFilter = null;
    _searchQuery = '';
    _sortBy = 'newest';
    loadProjects();
  }
}
