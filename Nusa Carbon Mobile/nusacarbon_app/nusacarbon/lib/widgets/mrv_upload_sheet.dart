import 'package:flutter/material.dart';
import '../constants/app_colors.dart';

class MrvUploadSheet extends StatefulWidget {
  final VoidCallback? onSubmit;
  const MrvUploadSheet({super.key, this.onSubmit});

  @override
  State<MrvUploadSheet> createState() => _MrvUploadSheetState();
}

class _MrvUploadSheetState extends State<MrvUploadSheet> {
  String? _selectedPeriod;
  final _gpsController = TextEditingController();
  final _satelliteController = TextEditingController();
  final _co2Controller = TextEditingController();
  final _notesController = TextEditingController();
  final _periods = ['2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4', '2025-Q1'];

  @override
  void dispose() { _gpsController.dispose(); _satelliteController.dispose(); _co2Controller.dispose(); _notesController.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return DraggableScrollableSheet(
      initialChildSize: 0.85, maxChildSize: 0.95, minChildSize: 0.5,
      builder: (_, scrollController) => Container(
        decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        child: ListView(controller: scrollController, padding: const EdgeInsets.all(20), children: [
          Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),
          const SizedBox(height: 16),
          const Text('Upload MRV Report', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
          const SizedBox(height: 20),
          DropdownButtonFormField<String>(
            initialValue: _selectedPeriod, items: _periods.map((p) => DropdownMenuItem(value: p, child: Text(p))).toList(),
            onChanged: (v) => setState(() => _selectedPeriod = v),
            decoration: const InputDecoration(labelText: 'Period'),
          ),
          const SizedBox(height: 12),
          TextField(controller: _gpsController, decoration: const InputDecoration(labelText: 'GPS Coordinates', hintText: '[{"lat":-1.6128,"lng":116.3542}]'), maxLines: 2),
          const SizedBox(height: 12),
          TextField(controller: _satelliteController, decoration: const InputDecoration(labelText: 'Satellite Photo Link', hintText: 'https://...')),
          const SizedBox(height: 12),
          TextField(controller: _co2Controller, decoration: const InputDecoration(labelText: 'Estimated CO₂e (tonnes)', hintText: '12500'), keyboardType: TextInputType.number),
          const SizedBox(height: 12),
          TextField(controller: _notesController, decoration: const InputDecoration(labelText: 'Notes', hintText: 'Add notes...'), maxLines: 3),
          const SizedBox(height: 16),
          OutlinedButton.icon(onPressed: () {}, icon: const Icon(Icons.upload_file), label: const Text('Upload Documents')),
          const SizedBox(height: 16),
          SizedBox(width: double.infinity, child: ElevatedButton(
            onPressed: () { widget.onSubmit?.call(); Navigator.pop(context); ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('MRV Report submitted'), backgroundColor: AppColors.primary)); },
            child: const Text('Submit MRV Report'),
          )),
          const SizedBox(height: 16),
        ]),
      ),
    );
  }
}
