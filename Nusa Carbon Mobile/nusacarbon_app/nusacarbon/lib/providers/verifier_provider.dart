import 'package:flutter/material.dart';
import '../models/mrv_report.dart';
import '../models/verification_model.dart';
import '../services/api_service.dart';

class VerifierProvider extends ChangeNotifier {
  List<MrvReport> _queue = [];
  List<VerificationModel> _auditLog = [];
  bool _isLoading = false;
  bool _isSubmitting = false;
  String? _submitError;

  List<MrvReport> get queue => _queue;
  List<VerificationModel> get auditLog => _auditLog;
  bool get isLoading => _isLoading;
  bool get isSubmitting => _isSubmitting;
  String? get submitError => _submitError;

  int get pendingCount =>
      _queue.where((m) => m.statusMrv == 'submitted').length;
  int get inReviewCount =>
      _queue.where((m) => m.statusMrv == 'under_review').length;
  int get approvedThisMonth =>
      _auditLog.where((v) => v.hasil == 'approved').length;

  // ─── Load ────────────────────────────────────────────────────────────

  Future<void> loadData(int userId) async {
    _isLoading = true;
    notifyListeners();

    try {
      final api = ApiService();

      // Pending MRV queue
      final queueRes = await api.getPendingMrv();
      if (queueRes.statusCode == 200) {
        final raw = queueRes.data['data'] as List?;
        if (raw != null) {
          _queue = raw.map((m) => MrvReport.fromJson(m as Map<String, dynamic>)).toList();
        }
      }

      // Audit log — verifications previously submitted by this verifier
      final logRes = await api.getVerificationsByVerifier(userId);
      if (logRes.statusCode == 200) {
        final raw = logRes.data['data'] as List?;
        if (raw != null) {
          _auditLog = raw
              .map((v) => VerificationModel.fromJson(v as Map<String, dynamic>))
              .toList();
        }
      }
    } catch (e) {
      debugPrint('VerifierProvider.loadData error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // ─── Submit Verification ─────────────────────────────────────────────

  /// Calls PUT /api/verifications/{mrvId} with the verifier decision.
  ///
  /// [hasil] must be one of: 'approved' | 'rejected' | 'revision_needed'
  ///
  /// Returns true on success. On success the MRV report is removed from
  /// [_queue] and a new [VerificationModel] is prepended to [_auditLog].
  Future<bool> submitVerification({
    required int mrvId,
    required int verifierId,
    required String hasil,
    double? volumeCo2eDisetujui,
    String? catatanAudit,
  }) async {
    _isSubmitting = true;
    _submitError = null;
    notifyListeners();

    try {
      final api = ApiService();
      final body = <String, dynamic>{
        'id_verifier': verifierId,
        'hasil': hasil,
        if (volumeCo2eDisetujui != null)
          'volume_co2e_disetujui': volumeCo2eDisetujui,
        if (catatanAudit != null && catatanAudit.isNotEmpty)
          'catatan_audit': catatanAudit,
      };

      final res = await api.submitVerification(mrvId, body);

      if (res.statusCode == 200) {
        final data = res.data['data'] as Map<String, dynamic>?;

        // Remove the reviewed MRV from the live queue
        _queue = _queue.where((m) => m.idMrv != mrvId).toList();

        // Prepend a new audit-log entry so it appears at the top
        if (data != null) {
          _auditLog = [
            VerificationModel(
              idVerifikasi: (data['id_verifikasi'] as num).toInt(),
              idMrv: (data['id_mrv'] as num).toInt(),
              idVerifier: verifierId,
              hasil: data['hasil'] as String,
              volumeCo2eDisetujui:
                  (data['volume_co2e_disetujui'] as num?)?.toDouble(),
              catatanAudit: data['catatan_audit'] as String?,
              verifiedAt: DateTime.parse(data['verified_at'] as String),
            ),
            ..._auditLog,
          ];
        }

        return true;
      } else {
        _submitError = 'Server returned ${res.statusCode}';
        return false;
      }
    } catch (e) {
      _submitError = e.toString();
      debugPrint('VerifierProvider.submitVerification error: $e');
      return false;
    } finally {
      _isSubmitting = false;
      notifyListeners();
    }
  }
}
