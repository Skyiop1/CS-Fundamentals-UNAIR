import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../models/carbon_token.dart';
import '../services/api_service.dart';

class TokensProvider extends ChangeNotifier {
  List<CarbonToken> _allTokens = [];
  String _searchQuery = '';
  String _activeTab = 'All';
  bool _isLoading = false;

  List<CarbonToken> get filteredTokens {
    var tokens = _allTokens;
    if (_activeTab != 'All') {
      if (_activeTab == 'Active') {
        tokens = tokens.where((t) => ['available', 'listed'].contains(t.statusToken)).toList();
      } else if (_activeTab == 'Retired') {
        tokens = tokens.where((t) => t.statusToken == 'retired').toList();
      } else if (_activeTab == 'Pending') {
        tokens = tokens.where((t) => t.statusToken == 'pending').toList();
      }
    }
    if (_searchQuery.isNotEmpty) {
      tokens = tokens.where((t) => t.namaProject.toLowerCase().contains(_searchQuery.toLowerCase())).toList();
    }
    return tokens;
  }

  String get activeTab => _activeTab;
  bool get isLoading => _isLoading;
  int get totalTokenCount => _allTokens.fold(0, (sum, t) => sum + (t.amount?.toInt() ?? 0));
  int get activeProjectCount => _allTokens.where((t) => t.statusToken == 'available' || t.statusToken == 'listed').map((t) => t.idProject).toSet().length;

  Future<void> loadTokens(int userId, {bool isDeveloper = false}) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      if (ApiService.useMock) {
        await Future.delayed(const Duration(milliseconds: 300));
        _allTokens = MockData.mockTokens;
      } else {
        final api = ApiService();
        // If developer mode, fetch tokens owned by this userId
        // If investor mode, fetch tokens in their portfolio (might be different endpoint or same with ownerId)
        final res = await api.getTokens(ownerId: userId);
        if (res.statusCode == 200) {
          final resData = res.data['data'] as List?;
          if (resData != null) {
            _allTokens = resData.map((t) => CarbonToken.fromJson(t)).toList();
          }
        }
      }
    } catch (e) {
      debugPrint('Error loading tokens: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void setTab(String tab) { _activeTab = tab; notifyListeners(); }
  void setSearch(String query) { _searchQuery = query; notifyListeners(); }
}
