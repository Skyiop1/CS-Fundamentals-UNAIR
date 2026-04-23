import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../models/carbon_project.dart';
import '../services/api_service.dart';

class HomeProvider extends ChangeNotifier {
  double _portfolioValue = MockData.portfolioValueIdr;
  double _totalTokens = MockData.totalTokens;
  double _monthlyChange = MockData.monthlyChange;
  List<CarbonProject> _activeProjects = [];
  List<double> _priceData = MockData.priceData7Day;
  bool _isLoading = false;

  double get portfolioValue => _portfolioValue;
  double get totalTokens => _totalTokens;
  double get monthlyChange => _monthlyChange;
  List<CarbonProject> get activeProjects => _activeProjects;
  List<double> get priceData => _priceData;
  List<String> get priceLabels => MockData.priceLabels7Day;
  bool get isLoading => _isLoading;

  Future<void> loadData(int userId) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      if (ApiService.useMock) {
        await Future.delayed(const Duration(milliseconds: 300));
        _activeProjects = MockData.mockProjects.where((p) => p.statusProject == 'verified').toList();
        _portfolioValue = MockData.portfolioValueIdr;
        _totalTokens = MockData.totalTokens;
        _monthlyChange = MockData.monthlyChange;
        _priceData = MockData.priceData7Day;
      } else {
        final api = ApiService();
        final projectsRes = await api.getProjects(status: 'verified');
        if (projectsRes.statusCode == 200) {
          final resData = projectsRes.data['data'] as List?;
          if (resData != null) {
            _activeProjects = resData.map((p) => CarbonProject.fromJson(p)).toList();
          }
        }
        
        final walletRes = await api.getWallet(userId);
        if (walletRes.statusCode == 200) {
          final wData = walletRes.data['data'];
          if (wData != null) {
            _totalTokens = (wData['total_tokens'] ?? wData['totalTokens'] ?? 0.0).toDouble();
            _portfolioValue = _totalTokens * MockData.tokenPriceIdr;
          }
        }
        
        // Price data might still be mock or from a separate endpoint if not in ApiService
        _priceData = MockData.priceData7Day;
        _monthlyChange = 8.2; // Example
      }
    } catch (e) {
      debugPrint('Error loading home data: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
