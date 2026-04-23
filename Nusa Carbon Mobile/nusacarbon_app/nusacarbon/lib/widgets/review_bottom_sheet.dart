import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../providers/verifier_provider.dart';

/// Bottom sheet for reviewing a single MRV report.
///
/// Calls [VerifierProvider.submitVerification] on approve / reject /
/// request-changes, then closes itself and invokes the matching callback
/// so the parent screen can show confirmation feedback.
class ReviewBottomSheet extends StatefulWidget {
  final int mrvId;
  final int verifierId;
  final String projectName;
  final String developerName;
  final String period;
  final double? estimatedCo2e;
  final VoidCallback? onApprove;
  final VoidCallback? onReject;
  final VoidCallback? onRequestChanges;

  const ReviewBottomSheet({
    super.key,
    required this.mrvId,
    required this.verifierId,
    required this.projectName,
    required this.developerName,
    required this.period,
    this.estimatedCo2e,
    this.onApprove,
    this.onReject,
    this.onRequestChanges,
  });

  @override
  State<ReviewBottomSheet> createState() => _ReviewBottomSheetState();
}

class _ReviewBottomSheetState extends State<ReviewBottomSheet> {
  double _mrvScore = 85;
  bool _satelliteValid = true;
  bool _aiAboveThreshold = true;
  bool _docsComplete = false;
  bool _noDoubleCounting = true;
  final _commentsController = TextEditingController();

  @override
  void dispose() {
    _commentsController.dispose();
    super.dispose();
  }

  // ─── Submit helper ────────────────────────────────────────────────────

  Future<void> _submit(BuildContext ctx, String hasil) async {
    final provider = ctx.read<VerifierProvider>();

    final ok = await provider.submitVerification(
      mrvId: widget.mrvId,
      verifierId: widget.verifierId,
      hasil: hasil,
      volumeCo2eDisetujui:
          widget.estimatedCo2e != null
              ? widget.estimatedCo2e! * (_mrvScore / 100)
              : null,
      catatanAudit:
          _commentsController.text.trim().isEmpty
              ? null
              : _commentsController.text.trim(),
    );

    if (!ctx.mounted) return;

    if (ok) {
      Navigator.of(ctx).pop();
      switch (hasil) {
        case 'approved':
          widget.onApprove?.call();
          break;
        case 'rejected':
          widget.onReject?.call();
          break;
        case 'revision_needed':
          widget.onRequestChanges?.call();
          break;
      }
    } else {
      // Show inline error without closing the sheet
      ScaffoldMessenger.of(ctx).showSnackBar(
        SnackBar(
          content: Text(
            provider.submitError ?? 'Submission failed. Please retry.',
          ),
          backgroundColor: AppColors.rejected,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  // ─── Build ────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final isSubmitting = context.watch<VerifierProvider>().isSubmitting;

    return DraggableScrollableSheet(
      initialChildSize: 0.85,
      maxChildSize: 0.95,
      minChildSize: 0.5,
      builder:
          (ctx, scrollController) => Container(
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
            ),
            child: ListView(
              controller: scrollController,
              padding: const EdgeInsets.all(20),
              children: [
                // ─── Handle ───────────────────────────────────────────
                Center(
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: AppColors.border,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // ─── Title ────────────────────────────────────────────
                const Text(
                  'Review MRV Report',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 16),

                // ─── Info rows ────────────────────────────────────────
                _infoRow('Project', widget.projectName),
                _infoRow('Developer', widget.developerName),
                _infoRow('Period', widget.period),
                _infoRow('MRV ID', '#${widget.mrvId}'),
                if (widget.estimatedCo2e != null)
                  _infoRow(
                    'Est. CO₂e',
                    '${widget.estimatedCo2e!.toStringAsFixed(0)} tCO₂e',
                  ),
                const SizedBox(height: 20),

                // ─── MRV Score slider ─────────────────────────────────
                const Text(
                  'MRV Score',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                ),
                Row(
                  children: [
                    Expanded(
                      child: Slider(
                        value: _mrvScore,
                        min: 0,
                        max: 100,
                        divisions: 100,
                        activeColor: _scoreColor(_mrvScore),
                        onChanged:
                            isSubmitting
                                ? null
                                : (v) => setState(() => _mrvScore = v),
                      ),
                    ),
                    Container(
                      width: 44,
                      alignment: Alignment.center,
                      child: Text(
                        '${_mrvScore.toInt()}',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: _scoreColor(_mrvScore),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 4),

                // ─── Checklist ────────────────────────────────────────
                _checkItem(
                  'Satellite data valid',
                  _satelliteValid,
                  isSubmitting
                      ? null
                      : (v) => setState(() => _satelliteValid = v!),
                ),
                _checkItem(
                  'AI score above threshold',
                  _aiAboveThreshold,
                  isSubmitting
                      ? null
                      : (v) => setState(() => _aiAboveThreshold = v!),
                ),
                _checkItem(
                  'Documentation complete',
                  _docsComplete,
                  isSubmitting
                      ? null
                      : (v) => setState(() => _docsComplete = v!),
                ),
                _checkItem(
                  'No double-counting risk',
                  _noDoubleCounting,
                  isSubmitting
                      ? null
                      : (v) => setState(() => _noDoubleCounting = v!),
                ),
                const SizedBox(height: 16),

                // ─── Comments ─────────────────────────────────────────
                TextField(
                  controller: _commentsController,
                  maxLines: 3,
                  enabled: !isSubmitting,
                  decoration: const InputDecoration(
                    labelText: 'Audit Comments',
                    hintText: 'Add review comments…',
                  ),
                ),
                const SizedBox(height: 24),

                // ─── Action buttons ───────────────────────────────────
                if (isSubmitting)
                  const Center(
                    child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 12),
                      child: CircularProgressIndicator(),
                    ),
                  )
                else
                  Row(
                    children: [
                      // Approve
                      Expanded(
                        child: ElevatedButton(
                          onPressed: () => _submit(context, 'approved'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                          child: const Text('Approve'),
                        ),
                      ),
                      const SizedBox(width: 8),
                      // Request changes
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () => _submit(context, 'revision_needed'),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: AppColors.pending,
                            side: const BorderSide(color: AppColors.pending),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                          child: const Text('Changes'),
                        ),
                      ),
                      const SizedBox(width: 8),
                      // Reject
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () => _submit(context, 'rejected'),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: AppColors.rejected,
                            side: const BorderSide(color: AppColors.rejected),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                          child: const Text('Reject'),
                        ),
                      ),
                    ],
                  ),
                const SizedBox(height: 8),
              ],
            ),
          ),
    );
  }

  // ─── Widget helpers ───────────────────────────────────────────────────

  Widget _infoRow(String label, String value) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
        ),
        Flexible(
          child: Text(
            value,
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
            textAlign: TextAlign.end,
          ),
        ),
      ],
    ),
  );

  Widget _checkItem(String label, bool value, ValueChanged<bool?>? onChanged) =>
      CheckboxListTile(
        value: value,
        onChanged: onChanged,
        title: Text(label, style: const TextStyle(fontSize: 14)),
        activeColor: AppColors.primary,
        contentPadding: EdgeInsets.zero,
        dense: true,
        controlAffinity: ListTileControlAffinity.leading,
      );

  Color _scoreColor(double score) {
    if (score >= 80) return AppColors.verified;
    if (score >= 60) return AppColors.pending;
    return AppColors.rejected;
  }
}
