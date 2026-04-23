import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../models/carbon_project.dart';
import '../models/mrv_report.dart';
import '../services/api_service.dart';

class OwnerProvider extends ChangeNotifier {
  List<CarbonProject> _projects = [];
  List<MrvReport> _mrvReports = [];
  bool _isLoading = false;

  List<CarbonProject> get projects => _projects;
  List<MrvReport> get mrvReports => _mrvReports;
  bool get isLoading => _isLoading;
  int get totalMinted => 23150;
  int get tokensSold => 8500;
  double get totalRevenue => 42500000;
  int get activeCount => _projects.where((p) => p.statusProject == 'verified').length;

  Future<void> loadData(int userId) async {
    _isLoading = true; notifyListeners();
    
    try {
      if (ApiService.useMock) {
        await Future.delayed(const Duration(milliseconds: 300));
        _projects = MockData.mockProjects;
        _mrvReports = MockData.mockMrvReports;
      } else {
        final api = ApiService();
        final projectsRes = await api.getProjects();
        if (projectsRes.statusCode == 200) {
          final pData = projectsRes.data['data'] as List?;
          if (pData != null) {
            final all = pData.map((p) => CarbonProject.fromJson(p)).toList();
            _projects = all.where((p) => p.idUser == userId).toList();
          }
        }
        
        _mrvReports = [];
        for (var p in _projects) {
          final mrvRes = await api.getMrvByProject(p.idProject);
          if (mrvRes.statusCode == 200) {
            final mData = mrvRes.data['data'] as List?;
            if (mData != null) {
              _mrvReports.addAll(mData.map((m) => MrvReport.fromJson(m)));
            }
          }
        }
      }
    } catch (e) {
      debugPrint('Error loading owner data: $e');
    } finally {
      _isLoading = false; notifyListeners();
    }
  }
}
