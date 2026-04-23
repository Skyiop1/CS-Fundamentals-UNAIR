import '../models/user_model.dart';
import '../models/wallet_model.dart';
import '../models/carbon_project.dart';
import '../models/carbon_token.dart';
import '../models/blockchain_tx.dart';
import '../models/listing.dart';
import '../models/mrv_report.dart';
import '../models/verification_model.dart';
import '../services/blockchain_service.dart';

/// All mock data for NusaCarbon during development (Week 1-5).
/// Switch to real API calls in Week 6+ by setting ApiService.useMock = false.
class MockData {
  MockData._();

  // ─── Mock User ──────────────────────────────────────────────────────
  static final UserModel mockUser = UserModel(
    idUser: 1,
    namaUser: 'PT Carbon Indonesia',
    email: 'carbonpt@nusacarbon.co.id',
    statusKyc: 'verified',
    roleName: 'investor',
    noHp: '+62 812 3456 7890',
    createdAt: DateTime(2024, 1, 15),
  );

  // ─── Mock Wallet ────────────────────────────────────────────────────
  static final WalletModel mockWallet = WalletModel(
    idWallet: 1,
    idUser: 1,
    walletAddress: '0x742d355Cc6634C853925a3b944fc9ef13a',
    chainNetwork: 'ethereum',
    createdAt: DateTime(2024, 1, 15),
  );

  // ─── Mock Projects (5 data) ─────────────────────────────────────────
  static final List<CarbonProject> mockProjects = [
    CarbonProject(
      idProject: 1,
      idUser: 2,
      idKategori: 2,
      namaProject: 'Mangrove Restoration Borneo',
      lokasi: 'Kalimantan, Indonesia',
      koordinatLat: -1.6128,
      koordinatLng: 116.3542,
      luasLahan: 15000,
      deskripsi:
          'Large-scale mangrove restoration across degraded coastal zones in East Kalimantan. '
          'The project aims to restore 15,000 hectares of mangrove habitat, sequestering an estimated '
          '450,000 tCO₂e over 10 years. Verified under Verra VCS standard with continuous dMRV '
          'monitoring via satellite imagery and AI-powered carbon estimation.',
      statusProject: 'verified',
      createdAt: DateTime(2024, 1, 10),
      updatedAt: DateTime(2024, 3, 15),
      namaKategori: 'Mangrove',
      imageUrl: 'https://images.unsplash.com/photo-1609137144813-7d9921338f24',
    ),
    CarbonProject(
      idProject: 2,
      idUser: 2,
      idKategori: 3,
      namaProject: 'Solar Farm Bali',
      lokasi: 'Bali, Indonesia',
      koordinatLat: -8.4095,
      koordinatLng: 115.1889,
      luasLahan: 500,
      deskripsi:
          'A 50MW solar photovoltaic installation in northern Bali, replacing coal-fired '
          'electricity generation. The project provides clean energy for over 30,000 households '
          'and reduces CO₂ emissions by an estimated 75,000 tCO₂e annually.',
      statusProject: 'verified',
      createdAt: DateTime(2024, 2, 5),
      updatedAt: DateTime(2024, 4, 10),
      namaKategori: 'Energi Terbarukan',
      imageUrl: 'https://images.unsplash.com/photo-1508514177221-188b1cf16e9d',
    ),
    CarbonProject(
      idProject: 3,
      idUser: 3,
      idKategori: 1,
      namaProject: 'Rainforest Conservation Sumatra',
      lokasi: 'Sumatra, Indonesia',
      koordinatLat: 0.5897,
      koordinatLng: 101.3431,
      luasLahan: 50000,
      deskripsi:
          'Protection of 50,000 hectares of primary tropical rainforest in central Sumatra. '
          'This REDD+ project prevents deforestation and degradation, conserving critical '
          'habitat for Sumatran orangutans, tigers, and elephants. Gold Standard certified.',
      statusProject: 'verified',
      createdAt: DateTime(2024, 3, 12),
      updatedAt: DateTime(2024, 5, 20),
      namaKategori: 'Hutan',
      imageUrl: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e',
    ),
    CarbonProject(
      idProject: 4,
      idUser: 4,
      idKategori: 3,
      namaProject: 'Wind Farm Java',
      lokasi: 'Jawa, Indonesia',
      koordinatLat: -7.5755,
      koordinatLng: 110.8243,
      luasLahan: 2000,
      deskripsi:
          'A 100MW onshore wind farm in eastern Java, consisting of 40 wind turbines. '
          'The project displaces fossil fuel-based power generation and is estimated to '
          'reduce emissions by 120,000 tCO₂e annually. Verified under Verra VCS.',
      statusProject: 'verified',
      createdAt: DateTime(2024, 4, 1),
      updatedAt: DateTime(2024, 6, 15),
      namaKategori: 'Energi Terbarukan',
      imageUrl: 'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51',
    ),
    CarbonProject(
      idProject: 5,
      idUser: 3,
      idKategori: 1,
      namaProject: 'Leuser Ecosystem Conservation',
      lokasi: 'Aceh, Indonesia',
      koordinatLat: 3.7500,
      koordinatLng: 97.5000,
      luasLahan: 26000,
      deskripsi:
          'Conservation of the Leuser Ecosystem, one of the most biodiverse areas on Earth. '
          'Home to Sumatran orangutans, rhinos, elephants, and tigers. The project covers '
          '26,000 hectares of protected forest under Plan Vivo standard.',
      statusProject: 'submitted',
      createdAt: DateTime(2024, 5, 20),
      namaKategori: 'Hutan',
      imageUrl: 'https://images.unsplash.com/photo-1511497584788-876760111969',
    ),
  ];

  // ─── Mock Tokens ────────────────────────────────────────────────────
  static final List<CarbonToken> mockTokens = [
    CarbonToken(
      idToken: 1,
      idProject: 1,
      idVerifikasi: 1,
      ownerUserId: 1,
      tokenSerial: 'NC-2024-001-000001',
      vintageYear: 2024,
      statusToken: 'available',
      txMintHash: BlockchainService.generateTxHash(
        previousHash: BlockchainService.genesisHash,
        type: 'mint',
        amount: 12500,
        refId: 1,
        timestamp: '2024-02-20T09:15:00Z',
      ),
      createdAt: DateTime(2024, 2, 20),
      namaProject: 'Mangrove Restoration Borneo',
      lokasi: 'Kalimantan, Indonesia',
      namaKategori: 'Mangrove',
      imageUrl: 'https://images.unsplash.com/photo-1609137144813-7d9921338f24',
      amount: 12500,
    ),
    CarbonToken(
      idToken: 2,
      idProject: 2,
      idVerifikasi: 2,
      ownerUserId: 1,
      tokenSerial: 'NC-2024-002-000001',
      vintageYear: 2024,
      statusToken: 'available',
      txMintHash: BlockchainService.generateTxHash(
        previousHash: BlockchainService.genesisHash,
        type: 'mint',
        amount: 7500,
        refId: 2,
        timestamp: '2024-03-10T11:30:00Z',
      ),
      createdAt: DateTime(2024, 3, 10),
      namaProject: 'Solar Farm Bali',
      lokasi: 'Bali, Indonesia',
      namaKategori: 'Energi Terbarukan',
      imageUrl: 'https://images.unsplash.com/photo-1508514177221-188b1cf16e9d',
      amount: 7500,
    ),
    CarbonToken(
      idToken: 3,
      idProject: 3,
      idVerifikasi: 3,
      ownerUserId: 1,
      tokenSerial: 'NC-2024-003-000001',
      vintageYear: 2024,
      statusToken: 'retired',
      txMintHash: BlockchainService.generateTxHash(
        previousHash: BlockchainService.genesisHash,
        type: 'mint',
        amount: 1650,
        refId: 3,
        timestamp: '2024-04-05T14:00:00Z',
      ),
      createdAt: DateTime(2024, 4, 5),
      namaProject: 'Rainforest Conservation Sumatra',
      lokasi: 'Sumatra, Indonesia',
      namaKategori: 'Hutan',
      imageUrl: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e',
      amount: 1650,
    ),
    CarbonToken(
      idToken: 4,
      idProject: 5,
      idVerifikasi: 0,
      ownerUserId: 1,
      tokenSerial: 'NC-2024-005-000001',
      vintageYear: 2024,
      statusToken: 'listed',
      createdAt: DateTime(2024, 6, 1),
      namaProject: 'Leuser Ecosystem Conservation',
      lokasi: 'Aceh, Indonesia',
      namaKategori: 'Hutan',
      imageUrl: 'https://images.unsplash.com/photo-1511497584788-876760111969',
      amount: 1500,
    ),
  ];

  // ─── Mock Blockchain Transactions ───────────────────────────────────
  static final List<BlockchainTx> mockBlockchainTxs = [
    BlockchainTx(
      hash: BlockchainService.generateTxHash(
        previousHash: BlockchainService.genesisHash,
        type: 'mint',
        amount: 10000,
        refId: 1,
        timestamp: '2024-02-20T09:15:00Z',
      ),
      previousHash: BlockchainService.genesisHash,
      timestamp: '2024-02-20T09:15:00Z',
      type: 'mint',
      amount: 10000,
      fromAddress: '0x0000000000000000000000000000000000000000',
      toAddress: '0x742d355Cc6634C853925a3b944fc9ef13a',
      blockNumber: 1,
      gasFeeMock: 0.005,
      projectName: 'Mangrove Restoration Borneo',
      status: 'confirmed',
    ),
    BlockchainTx(
      hash: BlockchainService.generateTxHash(
        previousHash: BlockchainService.genesisHash,
        type: 'transfer',
        amount: 2500,
        refId: 2,
        timestamp: '2024-02-18T14:32:00Z',
      ),
      previousHash: BlockchainService.genesisHash,
      timestamp: '2024-02-18T14:32:00Z',
      type: 'transfer',
      amount: 2500,
      fromAddress: '0x742d355Cc6634C853925a3b944fc9ef13a',
      toAddress: '0x8a3f2b9d1c4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a',
      blockNumber: 2,
      gasFeeMock: 0.003,
      projectName: 'Solar Farm Bali',
      status: 'confirmed',
    ),
    BlockchainTx(
      hash: BlockchainService.generateTxHash(
        previousHash: BlockchainService.genesisHash,
        type: 'retire',
        amount: 1500,
        refId: 3,
        timestamp: '2024-02-15T13:22:00Z',
      ),
      previousHash: BlockchainService.genesisHash,
      timestamp: '2024-02-15T13:22:00Z',
      type: 'retire',
      amount: 1500,
      fromAddress: '0x742d355Cc6634C853925a3b944fc9ef13a',
      toAddress: '0x0000000000000000000000000000000000000000',
      blockNumber: 3,
      gasFeeMock: 0.004,
      projectName: 'Rainforest Conservation Sumatra',
      status: 'confirmed',
    ),
  ];

  // ─── Mock Listings (Marketplace) ────────────────────────────────────
  static final List<Listing> mockListings = [
    Listing(
      idListing: 1,
      idUser: 2,
      idProject: 1,
      hargaPerToken: 5000,
      jumlahToken: 10000,
      statusListing: 'active',
      createdAt: DateTime(2024, 3, 1),
      namaProject: 'Mangrove Restoration Borneo',
      sellerName: 'PT Hijau Nusantara',
      namaKategori: 'Mangrove',
      lokasi: 'Kalimantan, Indonesia',
      imageUrl: 'https://images.unsplash.com/photo-1609137144813-7d9921338f24',
    ),
    Listing(
      idListing: 2,
      idUser: 2,
      idProject: 2,
      hargaPerToken: 5500,
      jumlahToken: 5000,
      statusListing: 'active',
      createdAt: DateTime(2024, 3, 15),
      namaProject: 'Solar Farm Bali',
      sellerName: 'PT Surya Energi',
      namaKategori: 'Energi Terbarukan',
      lokasi: 'Bali, Indonesia',
      imageUrl: 'https://images.unsplash.com/photo-1508514177221-188b1cf16e9d',
    ),
    Listing(
      idListing: 3,
      idUser: 3,
      idProject: 3,
      hargaPerToken: 4800,
      jumlahToken: 25000,
      statusListing: 'active',
      createdAt: DateTime(2024, 4, 1),
      namaProject: 'Rainforest Conservation Sumatra',
      sellerName: 'PT Rimba Lestari',
      namaKategori: 'Hutan',
      lokasi: 'Sumatra, Indonesia',
      imageUrl: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e',
    ),
    Listing(
      idListing: 4,
      idUser: 4,
      idProject: 4,
      hargaPerToken: 6000,
      jumlahToken: 8000,
      statusListing: 'active',
      createdAt: DateTime(2024, 5, 1),
      namaProject: 'Wind Farm Java',
      sellerName: 'PT Angin Jaya',
      namaKategori: 'Energi Terbarukan',
      lokasi: 'Jawa, Indonesia',
      imageUrl: 'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51',
    ),
    Listing(
      idListing: 5,
      idUser: 3,
      idProject: 5,
      hargaPerToken: 5200,
      jumlahToken: 15000,
      statusListing: 'active',
      createdAt: DateTime(2024, 6, 1),
      namaProject: 'Leuser Ecosystem Conservation',
      sellerName: 'PT Rimba Lestari',
      namaKategori: 'Hutan',
      lokasi: 'Aceh, Indonesia',
      imageUrl: 'https://images.unsplash.com/photo-1511497584788-876760111969',
    ),
  ];

  // ─── Mock MRV Reports (for Verifier Dashboard) ─────────────────────
  static final List<MrvReport> mockMrvReports = [
    MrvReport(
      idMrv: 1,
      idProject: 1,
      submittedBy: 2,
      periodeMrv: '2024-Q1',
      koordinatGps: '[{"lat":-1.6128,"lng":116.3542}]',
      linkFotoSatelit: 'https://satellite.example.com/borneo-q1',
      estimasiCo2e: 12500,
      catatan: 'Initial mangrove planting completed. Satellite imagery confirms seedling establishment.',
      statusMrv: 'submitted',
      createdAt: DateTime(2024, 4, 1),
      namaProject: 'Mangrove Restoration Borneo',
    ),
    MrvReport(
      idMrv: 2,
      idProject: 5,
      submittedBy: 3,
      periodeMrv: '2024-Q1',
      koordinatGps: '[{"lat":3.75,"lng":97.50}]',
      linkFotoSatelit: 'https://satellite.example.com/leuser-q1',
      estimasiCo2e: 8500,
      catatan: 'Forest canopy analysis shows 96% coverage. No deforestation detected.',
      statusMrv: 'under_review',
      createdAt: DateTime(2024, 4, 15),
      namaProject: 'Leuser Ecosystem Conservation',
    ),
    MrvReport(
      idMrv: 3,
      idProject: 3,
      submittedBy: 3,
      periodeMrv: '2024-Q2',
      koordinatGps: '[{"lat":0.5897,"lng":101.3431}]',
      linkFotoSatelit: 'https://satellite.example.com/sumatra-q2',
      estimasiCo2e: 15000,
      catatan: 'Quarterly monitoring report. Biomass measurement indicates strong growth.',
      statusMrv: 'submitted',
      createdAt: DateTime(2024, 7, 1),
      namaProject: 'Rainforest Conservation Sumatra',
    ),
  ];

  // ─── Mock Verifications (Audit Log) ─────────────────────────────────
  static final List<VerificationModel> mockVerifications = [
    VerificationModel(
      idVerifikasi: 1,
      idMrv: 1,
      idVerifier: 5,
      hasil: 'approved',
      volumeCo2eDisetujui: 12000,
      catatanAudit: 'Satellite data confirms planting. AI score above threshold (94%). Approved.',
      verifiedAt: DateTime(2024, 4, 20),
    ),
    VerificationModel(
      idVerifikasi: 2,
      idMrv: 2,
      idVerifier: 5,
      hasil: 'revision_needed',
      volumeCo2eDisetujui: null,
      catatanAudit: 'GPS coordinates need refinement. Please re-submit with updated polygon map.',
      verifiedAt: DateTime(2024, 5, 5),
    ),
  ];

  // ─── Mock KYC Users (for Admin Panel) ───────────────────────────────
  static final List<UserModel> mockKycQueue = [
    UserModel(
      idUser: 10,
      namaUser: 'CV Hijau Mandiri',
      email: 'hijau@mandiri.co.id',
      statusKyc: 'pending',
      roleName: 'project_owner',
      createdAt: DateTime(2024, 6, 10),
    ),
    UserModel(
      idUser: 11,
      namaUser: 'PT Bumi Lestari',
      email: 'admin@bumilestari.id',
      statusKyc: 'pending',
      roleName: 'investor',
      createdAt: DateTime(2024, 6, 12),
    ),
    UserModel(
      idUser: 12,
      namaUser: 'Yayasan Terumbu',
      email: 'info@terumbu.org',
      statusKyc: 'unverified',
      roleName: 'project_owner',
      createdAt: DateTime(2024, 6, 15),
    ),
  ];

  // ─── 7-Day Price Data (IDR per tCO₂e) ──────────────────────────────
  static const List<double> priceData7Day = [
    4600, 4750, 4900, 4850, 5100, 5050, 5000,
  ];

  static const List<String> priceLabels7Day = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
  ];

  // ─── Mock dMRV Chart Data (Quarterly CO₂ sequestration) ─────────────
  static const List<double> mrvQuarterlyData = [
    8500, 12000, 15500, 18000,
  ];

  static const List<String> mrvQuarterLabels = [
    'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024',
  ];

  static const List<double> satelliteConfidence = [92, 94, 96, 97];
  static const List<double> aiVerificationScore = [88, 91, 94, 96];

  // ─── Portfolio Summary ──────────────────────────────────────────────
  static const double totalTokens = 23150; // tCO₂e
  static const double portfolioValueIdr = 1248500000; // Rp 1,248,500,000
  static const double monthlyChange = 12.5; // +12.5%
  static const int activeProjects = 2;
  static const int pendingProjects = 1;
  static const double tokenPriceIdr = 5000; // Rp 5,000 per tCO₂e
}
