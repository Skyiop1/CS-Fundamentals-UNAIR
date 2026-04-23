import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';

class AdminProvider extends ChangeNotifier {
  List<UserModel> _kycQueue = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<UserModel> get kycQueue => _kycQueue;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  int get pendingCount => _kycQueue.length;

  Future<void> loadPendingKyc() async {
    _isLoading = true;
    _errorMessage = null;
    // Don't notify listeners yet to avoid unnecessary rebuilt if called during initState

    try {
      final api = ApiService();
      final res = await api.getUsers(kycStatus: 'pending');

      if (res.statusCode == 200) {
        final resData = res.data['data'] as List?;
        if (resData != null) {
          _kycQueue = resData.map((u) => UserModel.fromJson(u)).toList();
        }
      } else {
        _errorMessage = 'Failed to load KYC queue (Status: ${res.statusCode})';
      }
    } catch (e) {
      _errorMessage = 'Error loading KYC queue: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> updateKycStatus(int userId, String status) async {
    try {
      final api = ApiService();
      final res = await api.updateKycStatus(userId, status);

      if (res.statusCode == 200) {
        // Remove the user from the pending queue
        _kycQueue.removeWhere((u) => u.idUser == userId);
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      debugPrint('Error updating KYC status: $e');
      return false;
    }
  }
}
