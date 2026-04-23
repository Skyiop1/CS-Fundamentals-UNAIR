import 'package:dio/dio.dart';

/// REST API service using Dio.
///
/// Base URL: http://10.0.2.2:8080/api (Android emulator → localhost)
/// During development (Week 1-5): USE_MOCK = true
class ApiService {
  /// Toggle between mock data and real API calls.
  /// Set to `false` when backend is ready (Week 6+).
  static const bool useMock = false;

  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;

  late final Dio _dio;

  ApiService._internal() {
    _dio = Dio(
      BaseOptions(
        baseUrl: 'http://localhost:8080/api',
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Error interceptor
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Log request in debug mode
          // debugPrint('API Request: ${options.method} ${options.path}');
          handler.next(options);
        },
        onResponse: (response, handler) {
          handler.next(response);
        },
        onError: (error, handler) {
          final message = _getErrorMessage(error);
          // ignore: avoid_print
          print('API Error: $message');
          handler.next(error);
        },
      ),
    );
  }

  Dio get dio => _dio;

  // ─── Projects ───────────────────────────────────────────────────────
  Future<Response> getProjects({String? status, String? kategori}) async {
    return _dio.get(
      '/projects',
      queryParameters: {
        if (status != null) 'status': status,
        if (kategori != null) 'kategori': kategori,
      },
    );
  }

  Future<Response> getProjectById(int id) async {
    return _dio.get('/projects/$id');
  }

  Future<Response> createProject(Map<String, dynamic> data) async {
    return _dio.post('/projects', data: data);
  }

  // ─── Tokens ─────────────────────────────────────────────────────────
  Future<Response> getTokens({
    int? ownerId,
    String? status,
    int? vintage,
  }) async {
    return _dio.get(
      '/tokens',
      queryParameters: {
        if (ownerId != null) 'ownerId': ownerId,
        if (status != null) 'status': status,
        if (vintage != null) 'vintage': vintage,
      },
    );
  }

  Future<Response> getTokenById(int id) async {
    return _dio.get('/tokens/$id');
  }

  // ─── Listings / Marketplace ─────────────────────────────────────────
  Future<Response> getListings({String? kategori}) async {
    return _dio.get(
      '/listings',
      queryParameters: {if (kategori != null) 'kategori': kategori},
    );
  }

  // ─── Transactions ───────────────────────────────────────────────────
  Future<Response> buyTokens(Map<String, dynamic> data) async {
    return _dio.post('/transactions/buy', data: data);
  }

  Future<Response> getTransactions(int userId) async {
    return _dio.get('/transactions/$userId');
  }

  // ─── Retirements ────────────────────────────────────────────────────
  Future<Response> createRetirement(Map<String, dynamic> data) async {
    return _dio.post('/retirements', data: data);
  }

  Future<Response> getRetirements(int userId) async {
    return _dio.get('/retirements/$userId');
  }

  // ─── Certificates ──────────────────────────────────────────────────
  Future<Response> getCertificate(int retirementId) async {
    return _dio.get('/certificates/$retirementId');
  }

  // ─── Blockchain Ledger ─────────────────────────────────────────────
  /// [userId]    → filter entries by that user's wallet address (for Wallet screen)
  /// [projectId] → filter by project ref (for Project Detail ledger tab)
  /// No params   → return full ledger (admin use)
  Future<Response> getBlockchainLedger({int? userId, int? projectId}) async {
    return _dio.get(
      '/blockchain/ledger',
      queryParameters: {
        if (userId != null) 'userId': userId,
        if (projectId != null) 'projectId': projectId,
      },
    );
  }

  // ─── MRV ────────────────────────────────────────────────────────────
  Future<Response> submitMrvReport(Map<String, dynamic> data) async {
    return _dio.post('/mrv/submit', data: data);
  }

  Future<Response> getPendingMrv() async {
    return _dio.get('/mrv/pending');
  }

  Future<Response> getMrvByProject(int projectId) async {
    return _dio.get('/mrv/project/$projectId');
  }

  // ─── Verifications ─────────────────────────────────────────────────
  Future<Response> submitVerification(
    int mrvId,
    Map<String, dynamic> data,
  ) async {
    return _dio.put('/verifications/$mrvId', data: data);
  }

  /// Returns all verifications submitted by the given verifier (audit log).
  Future<Response> getVerificationsByVerifier(int verifierId) async {
    return _dio.get('/verifications/verifier/$verifierId');
  }

  // ─── Admin / Users ──────────────────────────────────────────────────
  Future<Response> getUserById(int id) async {
    return _dio.get('/users/$id');
  }

  Future<Response> getUsers({String? kycStatus}) async {
    return _dio.get(
      '/users',
      queryParameters: {if (kycStatus != null) 'kycStatus': kycStatus},
    );
  }

  Future<Response> updateKycStatus(int userId, String status) async {
    return _dio.put('/users/$userId/kyc', data: {'statusKyc': status});
  }

  // ─── Wallet ─────────────────────────────────────────────────────────
  Future<Response> getWallet(int userId) async {
    return _dio.get('/wallet/$userId');
  }

  // ─── Error Handling ─────────────────────────────────────────────────
  String _getErrorMessage(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
        return 'Connection timeout. Please check your internet.';
      case DioExceptionType.receiveTimeout:
        return 'Server took too long to respond.';
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode ?? 0;
        if (statusCode == 404) return 'Resource not found.';
        if (statusCode == 500) return 'Internal server error.';
        return 'Server error ($statusCode).';
      case DioExceptionType.connectionError:
        return 'Could not connect to server.';
      default:
        return 'An unexpected error occurred.';
    }
  }
}
