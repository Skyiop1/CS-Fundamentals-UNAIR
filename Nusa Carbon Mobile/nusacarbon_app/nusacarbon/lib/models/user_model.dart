class UserModel {
  final int idUser;
  final String namaUser;
  final String email;
  final String statusKyc; // unverified | pending | verified | rejected
  final String roleName; // project_owner | investor | verifier | admin
  final String? noHp;
  final DateTime createdAt;

  const UserModel({
    required this.idUser,
    required this.namaUser,
    required this.email,
    required this.statusKyc,
    required this.roleName,
    this.noHp,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      idUser: json['id_user'] as int,
      namaUser: json['nama_user'] as String,
      email: json['email'] as String,
      statusKyc: json['status_kyc'] as String,
      roleName: json['role_name'] as String,
      noHp: json['no_hp'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_user': idUser,
      'nama_user': namaUser,
      'email': email,
      'status_kyc': statusKyc,
      'role_name': roleName,
      'no_hp': noHp,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
