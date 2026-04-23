import 'package:flutter/material.dart';
import '../models/listing.dart';
import '../services/api_service.dart';

/// Manages marketplace listings with server-side category filtering.
///
/// Category filter → passed as ?kategori= query param to GET /api/listings
/// Search & sort   → applied client-side on the already-filtered result set
class MarketplaceProvider extends ChangeNotifier {
  List<Listing> _listings = [];
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
  List<Listing> get filteredListings {
    var list = List<Listing>.from(_listings);

    // Client-side search (server has no full-text search endpoint)
    if (_searchQuery.isNotEmpty) {
      final q = _searchQuery.toLowerCase();
      list =
          list
              .where(
                (l) =>
                    l.namaProject.toLowerCase().contains(q) ||
                    (l.lokasi?.toLowerCase().contains(q) ?? false) ||
                    (l.namaKategori?.toLowerCase().contains(q) ?? false),
              )
              .toList();
    }

    // Client-side sort
    switch (_sortBy) {
      case 'price_low':
        list.sort((a, b) => a.hargaPerToken.compareTo(b.hargaPerToken));
        break;
      case 'price_high':
        list.sort((a, b) => b.hargaPerToken.compareTo(a.hargaPerToken));
        break;
      case 'newest':
      default:
        list.sort((a, b) => b.createdAt.compareTo(a.createdAt));
        break;
    }

    return list;
  }

  // ─── Load ────────────────────────────────────────────────────────────────

  /// Fetches listings from the API.
  ///
  /// When [_categoryFilter] is set it is sent as a ?kategori= query param so
  /// the server returns only matching listings — no client-side category
  /// filtering needed afterwards.
  Future<void> loadListings(int userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final api = ApiService();
      final res = await api.getListings(kategori: _categoryFilter);

      if (res.statusCode == 200) {
        final raw = res.data['data'] as List?;
        if (raw != null) {
          _listings =
              raw
                  .map((l) => Listing.fromJson(l as Map<String, dynamic>))
                  .toList();
        }
      } else {
        _error = 'Server returned ${res.statusCode}';
      }
    } catch (e) {
      _error = e.toString();
      debugPrint('MarketplaceProvider.loadListings error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // ─── Filter / Sort controls ──────────────────────────────────────────────

  /// Sets the category filter and immediately reloads from the API so the
  /// result set is filtered server-side (not just in memory).
  void setCategory(String? cat, int userId) {
    if (_categoryFilter == cat) return; // no-op if unchanged
    _categoryFilter = cat;
    loadListings(userId); // triggers _isLoading + notifyListeners inside
  }

  void setSortBy(String sort) {
    _sortBy = sort;
    notifyListeners();
  }

  void setSearch(String q) {
    _searchQuery = q;
    notifyListeners();
  }

  void clearFilters(int userId) {
    _categoryFilter = null;
    _searchQuery = '';
    _sortBy = 'newest';
    loadListings(userId);
  }
}
