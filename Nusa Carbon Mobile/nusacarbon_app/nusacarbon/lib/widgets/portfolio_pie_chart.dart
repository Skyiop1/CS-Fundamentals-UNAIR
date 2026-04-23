import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../constants/app_colors.dart';

class PortfolioPieChart extends StatelessWidget {
  final List<PieChartEntry> entries;
  const PortfolioPieChart({super.key, required this.entries});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: 180,
          child: PieChart(PieChartData(
            sections: entries.asMap().entries.map((e) {
              final i = e.key;
              final d = e.value;
              return PieChartSectionData(
                value: d.value,
                title: '${d.percentage.toStringAsFixed(0)}%',
                color: AppColors.pieColors[i % AppColors.pieColors.length],
                radius: 40,
                titleStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
              );
            }).toList(),
            sectionsSpace: 2,
            centerSpaceRadius: 45,
          )),
        ),
        const SizedBox(height: 16),
        Wrap(
          spacing: 16,
          runSpacing: 8,
          children: entries.asMap().entries.map((e) {
            final i = e.key;
            final d = e.value;
            return Row(mainAxisSize: MainAxisSize.min, children: [
              Container(width: 10, height: 10, decoration: BoxDecoration(color: AppColors.pieColors[i % AppColors.pieColors.length], borderRadius: BorderRadius.circular(2))),
              const SizedBox(width: 6),
              Text(d.label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
            ]);
          }).toList(),
        ),
      ],
    );
  }
}

class PieChartEntry {
  final String label;
  final double value;
  final double percentage;
  const PieChartEntry({required this.label, required this.value, required this.percentage});
}
