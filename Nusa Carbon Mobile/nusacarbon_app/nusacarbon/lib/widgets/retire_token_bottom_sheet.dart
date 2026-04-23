import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../constants/app_colors.dart';
import '../models/carbon_token.dart';
import '../providers/account_provider.dart';
import '../services/api_service.dart';

class RetireTokenBottomSheet extends StatefulWidget {
  final CarbonToken token;
  final VoidCallback onSuccess;

  const RetireTokenBottomSheet({
    super.key,
    required this.token,
    required this.onSuccess,
  });

  @override
  State<RetireTokenBottomSheet> createState() => _RetireTokenBottomSheetState();
}

class _RetireTokenBottomSheetState extends State<RetireTokenBottomSheet> {
  final _reasonController = TextEditingController();
  final _entityController = TextEditingController();
  bool _isLoading = false;
  String? _error;

  @override
  void dispose() {
    _reasonController.dispose();
    _entityController.dispose();
    super.dispose();
  }

  Future<void> _submitRetirement() async {
    final reason = _reasonController.text.trim();
    final entity = _entityController.text.trim();

    if (reason.isEmpty || entity.isEmpty) {
      setState(() => _error = 'Please fill in all fields');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    final userId = context.read<AccountProvider>().currentUserId;

    try {
      final res = await ApiService().createRetirement({
        'user_id': userId,
        'token_ids': [widget.token.idToken],
        'alasan': reason,
        'nama_entitas': entity,
      });

      if (res.statusCode == 201) {
        if (mounted) {
          Navigator.pop(context);
          _showSuccessDialog();
          widget.onSuccess();
        }
      } else {
        setState(() => _error = 'Failed to retire token. Status: ${res.statusCode}');
      }
    } catch (e) {
      setState(() => _error = 'An error occurred. Please try again.');
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  void _showSuccessDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        contentPadding: const EdgeInsets.all(24),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Icon(Icons.check_circle, size: 64, color: AppColors.verified),
            const SizedBox(height: 16),
            const Text(
              'Tokens Retired!',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textPrimary),
            ),
            const SizedBox(height: 8),
            Text(
              'Token ${widget.token.tokenSerial} has been successfully retired for ${_entityController.text.trim()}.',
              textAlign: TextAlign.center,
              style: const TextStyle(color: AppColors.textSecondary),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                child: const Text('Back to Token Details'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 24,
        right: 24,
        top: 24,
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
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
          const SizedBox(height: 20),
          const Text(
            'Retire Carbon Token',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          const Text(
            'Retiring a token removes it from circulation and creates an offset certificate.',
            style: TextStyle(fontSize: 14, color: AppColors.textSecondary),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          const Text('Retirement Details', style: TextStyle(fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
          const SizedBox(height: 12),
          TextField(
            controller: _entityController,
            decoration: const InputDecoration(
              labelText: 'Beneficiary Entity Name',
              hintText: 'e.g., PT Global Nusantara',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _reasonController,
            decoration: const InputDecoration(
              labelText: 'Reason for Retirement',
              hintText: 'e.g., Scope 1 Offset 2024',
              border: OutlineInputBorder(),
            ),
          ),
          if (_error != null) ...[
            const SizedBox(height: 16),
            Text(_error!, style: const TextStyle(color: AppColors.rejected, fontSize: 14)),
          ],
          const SizedBox(height: 24),
          SizedBox(
            height: 50,
            child: ElevatedButton(
              onPressed: _isLoading ? null : _submitRetirement,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.rejected,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
              child: _isLoading
                  ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                  : const Text('Confirm Retirement'),
            ),
          ),
        ],
      ),
    );
  }
}
