import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../constants/app_colors.dart';
import '../data/mock_data.dart';
import '../models/user_model.dart';
import '../widgets/status_badge.dart';

class AdminScreen extends StatefulWidget {
  const AdminScreen({super.key});

  @override
  State<AdminScreen> createState() => _AdminScreenState();
}

class _AdminScreenState extends State<AdminScreen> {
  final List<UserModel> _kycQueue = List.from(MockData.mockKycQueue);
  bool _isLoading = false;

  void _processKyc(UserModel user, bool approve) {
    setState(() {
      _kycQueue.remove(user);
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          approve
              ? 'KYC Approved for ${user.namaUser}'
              : 'KYC Rejected for ${user.namaUser}',
        ),
        backgroundColor: approve ? AppColors.verified : AppColors.rejected,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Admin Panel'),
          actions: [
            Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Chip(
                label: const Text(
                  'Admin',
                  style: TextStyle(
                    color: AppColors.dark,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                backgroundColor: AppColors.dark.withValues(alpha: 0.1),
                side: BorderSide.none,
              ),
            ),
          ],
          bottom: const TabBar(
            tabs: [Tab(text: 'KYC Queue'), Tab(text: 'User Management')],
          ),
        ),
        body: TabBarView(
          children: [
            // KYC Queue Tab
            _isLoading
                ? const Center(child: CircularProgressIndicator())
                : RefreshIndicator(
                  onRefresh: () async {
                    setState(() => _isLoading = true);
                    await Future.delayed(const Duration(milliseconds: 500));
                    setState(() {
                      _kycQueue.clear();
                      _kycQueue.addAll(MockData.mockKycQueue);
                      _isLoading = false;
                    });
                  },
                  child:
                      _kycQueue.isEmpty
                          ? const Center(
                            child: Padding(
                              padding: EdgeInsets.all(24),
                              child: Text(
                                'No pending KYC applications.',
                                style: TextStyle(color: AppColors.textMuted),
                              ),
                            ),
                          )
                          : ListView.builder(
                            padding: const EdgeInsets.all(16),
                            itemCount: _kycQueue.length,
                            itemBuilder: (context, index) {
                              final user = _kycQueue[index];
                              return Card(
                                margin: const EdgeInsets.only(bottom: 12),
                                child: Padding(
                                  padding: const EdgeInsets.all(16),
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        children: [
                                          Expanded(
                                            child: Text(
                                              user.namaUser,
                                              style: const TextStyle(
                                                fontSize: 16,
                                                fontWeight: FontWeight.bold,
                                                color: AppColors.textPrimary,
                                              ),
                                            ),
                                          ),
                                          StatusBadge(status: user.statusKyc),
                                        ],
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        user.email,
                                        style: const TextStyle(
                                          fontSize: 14,
                                          color: AppColors.textSecondary,
                                        ),
                                      ),
                                      const SizedBox(height: 12),
                                      Row(
                                        children: [
                                          const Icon(
                                            Icons.date_range,
                                            size: 14,
                                            color: AppColors.textMuted,
                                          ),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Submitted: ${DateFormat('MMM d, yyyy').format(user.createdAt)}',
                                            style: const TextStyle(
                                              fontSize: 12,
                                              color: AppColors.textMuted,
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 8),
                                      const Row(
                                        children: [
                                          Icon(
                                            Icons.description,
                                            size: 14,
                                            color: AppColors.textMuted,
                                          ),
                                          SizedBox(width: 4),
                                          Text(
                                            '3 Documents attached',
                                            style: TextStyle(
                                              fontSize: 12,
                                              color: AppColors.textMuted,
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 16),
                                      Row(
                                        children: [
                                          Expanded(
                                            child: ElevatedButton(
                                              onPressed:
                                                  () => _processKyc(user, true),
                                              style: ElevatedButton.styleFrom(
                                                backgroundColor:
                                                    AppColors.verified,
                                              ),
                                              child: const Text('Approve KYC'),
                                            ),
                                          ),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: OutlinedButton(
                                              onPressed:
                                                  () =>
                                                      _processKyc(user, false),
                                              style: OutlinedButton.styleFrom(
                                                foregroundColor:
                                                    AppColors.rejected,
                                                side: const BorderSide(
                                                  color: AppColors.rejected,
                                                ),
                                              ),
                                              child: const Text('Reject'),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                ),

            // User Management Tab
            ListView(
              padding: const EdgeInsets.all(16),
              children: [
                const TextField(
                  decoration: InputDecoration(
                    hintText: 'Search users...',
                    prefixIcon: Icon(Icons.search),
                    filled: true,
                    fillColor: Colors.white,
                  ),
                ),
                const SizedBox(height: 24),

                // MOCK USER LIST
                _UserListItem(user: MockData.mockUser),
                const Divider(),
                _UserListItem(
                  user: UserModel(
                    idUser: 2,
                    namaUser: 'Budi Santoso',
                    email: 'budi@example.com',
                    statusKyc: 'unverified',
                    roleName: 'buyer',
                    createdAt: DateTime(2024, 2, 10),
                  ),
                ),
                const Divider(),
                _UserListItem(
                  user: UserModel(
                    idUser: 3,
                    namaUser: 'PT Energi Hijau',
                    email: 'contact@energihijau.id',
                    statusKyc: 'verified',
                    roleName: 'project_owner',
                    createdAt: DateTime(2024, 3, 5),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _UserListItem extends StatelessWidget {
  final UserModel user;

  const _UserListItem({required this.user});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: CircleAvatar(
        backgroundColor: AppColors.primary.withValues(alpha: 0.1),
        child: Text(
          user.namaUser[0].toUpperCase(),
          style: const TextStyle(
            color: AppColors.primary,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      title: Text(
        user.namaUser,
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
      subtitle: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(user.email, style: const TextStyle(fontSize: 12)),
          const SizedBox(height: 4),
          Row(
            children: [
              StatusBadge(status: user.statusKyc, fontSize: 10),
              const SizedBox(width: 6),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: AppColors.border,
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  user.roleName,
                  style: const TextStyle(
                    fontSize: 10,
                    color: AppColors.textSecondary,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
      trailing: IconButton(
        icon: const Icon(Icons.more_vert),
        onPressed: () {
          _showUserOptions(context);
        },
      ),
    );
  }

  void _showUserOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder:
          (context) => SafeArea(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text('View Profile'),
                  onTap: () => Navigator.pop(context),
                ),
                ListTile(
                  leading: const Icon(Icons.admin_panel_settings),
                  title: const Text('Change Role'),
                  onTap: () => Navigator.pop(context),
                ),
                ListTile(
                  leading: const Icon(Icons.block, color: AppColors.rejected),
                  title: const Text(
                    'Suspend Account',
                    style: TextStyle(color: AppColors.rejected),
                  ),
                  onTap: () => Navigator.pop(context),
                ),
              ],
            ),
          ),
    );
  }
}
