# System Instructions: NusaCarbon — Flutter Mobile App v2
# Nusantara Carbon Token Exchange Platform

## Project Overview

Build **NusaCarbon**, a Flutter mobile application implementing a blockchain-inspired carbon credit token marketplace for Indonesia. The platform tokenizes verified carbon credits from Indonesian conservation and clean-energy projects — **1 token = 1 tCO₂e** — enabling transparent buying, selling, and retirement of carbon credits with a simulated on-chain ledger.

**Core concept:** NusaCarbon does NOT sell land or physical projects. It tokenizes verified CO₂ sequestration. Each token is "minted" only after a Verifier approves the MRV (Measurement, Reporting & Verification) report. Token retirement permanently removes the token from circulation — preventing double offset claims.

**Blockchain approach (prototype simulation):**
- No real blockchain integration
- SHA-256 hash generation (Dart `crypto` package) creates deterministic, immutable-looking transaction hashes
- Append-only ledger: MySQL `blockchain_ledger` table — no UPDATE/DELETE allowed
- Sequential block linking: each record stores the hash of the previous record
- Wallet addresses are mock strings (format: `0x742d...8f3a`)
- Gas fees are mock values shown for realism (e.g., `~0.004 ETH`)

**Currency:** All prices and portfolio values displayed in **IDR (Indonesian Rupiah)**
- Format: `Rp 1,248,500,000` (use `NumberFormat.currency(locale: 'id_ID', symbol: 'Rp ')`)
- Token price reference: `Rp 5,000 per tCO₂e`

**Architecture:** Flutter → REST API (Spring Boot / Java) → MySQL

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Flutter (Dart) |
| State Management | Provider (`provider` package) |
| HTTP Client | Dio (`dio` package) |
| Local Storage | SharedPreferences (`shared_preferences` package) |
| Charts | fl_chart (`fl_chart` package) |
| Navigation | GoRouter (`go_router` package) |
| Hashing | `crypto` package (SHA-256 for blockchain simulation) |
| Date Formatting | `intl` package |
| Image Caching | `cached_network_image` package |
| Backend | REST API — Spring Boot (Java) |
| Database | MySQL |
| Dev Tools | XAMPP / Laragon, VS Code, Git/GitHub |

### pubspec.yaml Dependencies
```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.2
  dio: ^5.4.0
  shared_preferences: ^2.2.2
  go_router: ^13.2.0
  fl_chart: ^0.68.0
  crypto: ^3.0.3
  intl: ^0.19.0
  cached_network_image: ^3.3.1
```

---

## Actors / Roles

| Role | Description |
|---|---|
| **Project Owner** | Pengelola lahan/teknologi hijau. Mendaftarkan proyek, mengunggah dokumen MRV, menerima hasil tokenisasi. |
| **Verifier (Auditor)** | Pihak independen (referensi: OJK). Memeriksa kelayakan data MRV dan memberikan persetujuan penerbitan token. |
| **Buyer** | Individu atau korporasi. Membeli token untuk investasi hijau atau pemenuhan target Net Zero. Bisa melakukan retirement. |
| **Admin** | Pengelola platform. Bertanggung jawab atas verifikasi identitas (KYC/AML) dan pemeliharaan infrastruktur sistem. |

---

## Navigation Structure

### Bottom Navigation Bar (Global — all authenticated users)
```
Home  |  Tokens  |  Wallet  |  Profile
 🏠        📊        💳        👤
```

All roles share the same bottom nav. Screen content adapts based on role stored in SharedPreferences.

### Routes
| Path | Screen | Description |
|---|---|---|
| `/splash` | `SplashScreen` | Logo animation + role selection |
| `/home` | `HomeScreen` | Dashboard: portfolio value, active projects, quick actions |
| `/tokens` | `TokensScreen` | My Tokens list: All · Active · Retired · Pending tabs |
| `/tokens/:tokenId` | `TokenDetailScreen` | Single token detail |
| `/marketplace` | `MarketplaceScreen` | Browse & filter all listed token batches |
| `/project/:projectId` | `ProjectDetailScreen` | Project detail + MRV data + buy widget |
| `/wallet` | `WalletScreen` | Connected wallet, total balance, transaction history |
| `/profile` | `ProfileScreen` | User info, KYC status, org details, linked wallet |
| `/dashboard/verifier` | `VerifierDashboardScreen` | Task queue (Verifier role only — accessible from Profile) |
| `/dashboard/owner` | `OwnerDashboardScreen` | Project management (Project Owner role — from Profile) |
| `/admin` | `AdminScreen` | KYC approval queue (Admin role — from Profile) |

---

## Screen Specifications

### 1. Splash / Role Selection Screen

- NusaCarbon logo (Leaf icon + wordmark) centered with fade-in animation
- Tagline: "Transparent. Verified. Tokenized Carbon Credits."
- Role selection buttons (full-width, stacked):
  - **Buyer** (emerald fill)
  - **Project Owner** (teal fill)
  - **Verifier** (indigo outline)
  - **Admin** (slate outline)
- Role saved to SharedPreferences
- "Explore as Guest" text button → `/marketplace` (limited, no buy/retire)

---

### 2. Home Screen (`/home`)

#### AppBar
- Left: NusaCarbon logo (icon + wordmark)
- Right: Notification bell icon (with badge count) + Settings gear icon

#### Portfolio Hero Card (full-width, emerald gradient)
```
Total Portfolio Value
Rp 1,248,500,000
↗ +12.5% this month

Carbon Tokens Held
23,150 tCO₂e     [Portfolio icon button]
```

#### Token Price Chart (7-day)
- LineChart (fl_chart): 7-day token price in IDR
- Label: "Token Price (7D)" + percentage change chip (e.g., `↑ +8.2%`)
- X-axis: Mon Tue Wed Thu Fri Sat Sun
- Y-axis: IDR (abbreviated: 0, 15, 30, 45, 60)
- Caption: `Current: Rp 5,000 per tCO₂e`

#### Quick Actions Row (4 icon buttons)
```
[Tokenize]   [Retire]   [Transfer]
    ↑            🔥          ↗
```
- Tokenize → visible only for Project Owner role
- Retire → `/tokens` (with retire filter)
- Transfer → simulated transfer flow

#### Active Projects Section
- Header: "Active Projects" + "View All" text button
- `ListView` (horizontal scroll, 2 items visible):
  - Project image (CachedNetworkImage, 120px height)
  - "Active" badge (emerald)
  - Project name
  - Location (with pin icon)
  - "Your Tokens: X tCO₂e"

---

### 3. Tokens Screen — My Tokens (`/tokens`)

#### AppBar
- Back arrow (if navigated from elsewhere)
- Title: "My Tokens"
- Filter icon → opens FilterBottomSheet
- Search bar (expandable): "Search projects..."

#### Summary Stats Row (2 cards)
```
Total Tokens     Active Projects
23,150 tCO₂e    2 (+1 pending)
```

#### Tab Bar
```
All  |  Active  |  Retired  |  Pending
```

#### Token List (`ListView.builder`)
Each token item card:
- Project image (120px height, cover, with status badge overlay)
- Status badge: `Active` (emerald) · `Retired` (red) · `Pending` (amber)
- Verification badge: `VERRA VCS` or `GOLD STANDARD` (outlined, small)
- Project name (bold)
- Location (MapPin icon + city, province)
- Row: Amount (`12,500 tCO₂e`) · Vintage (`2024`) · Token ID (`0x742d...8f3a`, monospace)
- Tap → `TokenDetailScreen`

---

### 4. Wallet Screen (`/wallet`)

#### AppBar
- Title: "Wallet"

#### Connected Wallet Card (dark/slate background)
```
Connected Wallet
0x742d...8f3a     [Copy icon]  [Edit icon]
```

#### Balance Display (centered, large)
```
Total Balance
23,150
tCO₂e Carbon Tokens
```

#### Action Buttons Row
```
[Receive ↙]   [Send ↗]   [Swap ⇄]
```
All three → show mock modal (no real functionality):
- Receive: shows wallet address QR-style display
- Send: shows address input + amount input → generates mock tx hash
- Swap: shows "Coming Soon" dialog

#### Transaction History Section
- Header: "Transaction History" + "View All" button
- `ListView` of blockchain transactions:
  ```
  [↗] Mint  ✓ Confirmed          +10,000 tCO₂e
      Mangrove Restoration Borneo   2024-02-20 · 09:15
      0x#abc123def456...
      Gas Fee: 0.005 ETH

  [↙] Transfer  ✓ Confirmed       -2,500 tCO₂e
      Solar Farm Bali               2024-02-18 · 14:32
      0x#ade456gh1789...
      Gas Fee: 0.003 ETH

  [🔥] Retire  ✓ Confirmed        -1,500 tCO₂e
      Rainforest Conservation       2024-02-15 · 13:22
      0x#7B89j1812mo345...
      Gas Fee: 0.004 ETH
  ```
- Transaction type icons: `↗` mint (emerald) · `↙` transfer (blue) · `🔥` retire (red)
- Status: "✓ Confirmed" (green text) · "⏳ Pending" (amber)
- Mock ETH gas fees shown for every transaction

---

### 5. Profile Screen (`/profile`)

#### Header
```
← Profile

[Avatar circle — person icon]
PT Carbon Indonesia
carbonpt@nusacarbon.co.id

Verification Status: ✓ Verified
```

#### KYC Checklist (ListTile items with icons)
- ✅ Identity Verification
- ✅ Business Documentation
- ✅ Bank Account
- ✅ Wallet Connection
- Each row is tappable → detail/upload screen (mock)

#### Role Toggle (for Buyer/Project Owner dual-role)
```
[Customer]   [Seller]
```
Segmented button — changes dashboard view context

#### Organization Details Card
```
Company Name: PT Carbon Indonesia
Business Type: Carbon Project Developer
Registration Number: ID-2024-#123456
Location: Jakarta, Indonesia
Member Since: January 2024
Account Type: Token Provider (chip)
[Edit Organization Info]
```

#### Linked Blockchain Wallet Card
```
[MetaMask icon]  MetaMask          ● Active
                 Ethereum Mainnet
  0x742d355Cc6634C853925a3b944fc9ef13a
  [Change Wallet]
```

#### Settings Links (ListTile)
- 🔔 Notifications (badge: 2)
- 🔒 Security & Privacy
- ❓ Help & Support

#### Role-specific Dashboard Links
- Project Owner → "Manage Projects" button → `OwnerDashboardScreen`
- Verifier → "Verification Queue" button → `VerifierDashboardScreen`
- Admin → "Admin Panel" button → `AdminScreen`

#### Log Out Button (full-width, red outlined)
```
[→ Log Out]
```
Clears SharedPreferences → navigates to `/splash`

#### App Version
```
NusaCarbon v1.0.0
```

---

### 6. Project Detail Screen (`/project/:projectId`)

#### AppBar
- Back arrow → Marketplace / Tokens
- Title: project name (truncated)
- Share icon (mock)

#### Hero Image
- CachedNetworkImage, height: 220px, full width, BoxFit.cover
- Status badge overlay (Active/Pending/Retired)
- Verification standard badge (Verra VCS / Gold Standard / Plan Vivo)

#### Info Section (Card)
- Project name (h1)
- Location: `📍 Kalimantan, Indonesia`
- Amount · Vintage · Token ID row (same as token list card)
- Description paragraph

#### Tabbed Section (3 tabs)

**Tab 1: dMRV Data**
- LineChart (fl_chart): quarterly CO₂ sequestration
- Satellite Confidence % → LinearProgressIndicator (emerald)
- AI Verification Score % → LinearProgressIndicator (teal)
- Data table: Quarter · CO₂ Sequestered · Satellite Conf. · AI Score

**Tab 2: Blockchain Ledger**
- ListView of on-chain transactions:
  - Hash (truncated monospace + copy icon)
  - Type chip: `mint` · `transfer` · `retire`
  - Amount tCO₂e
  - From → To (truncated)
  - Timestamp
- Network Gas Fee shown per transaction

**Tab 3: Project Info**
- Full description
- Project Owner details
- Coordinates (lat/lng)
- SDG badges
- Verification body + date
- Documents (mock tappable): Validation Report, MRV Methodology, PDD

#### Buy / Tokenize Widget (bottom sticky)
- Vintage year
- Price: `Rp 5,000 per tCO₂e`
- Quantity input (min: 1)
- Calculated total: `X tokens × Rp 5,000 = Rp XX,XXX,XXX`
- Equivalency: `= X tCO₂e offset`
- "Buy Tokens" CTA (emerald, full width)
- On tap → mock success BottomSheet + generated tx hash + gas fee

---

### 7. Verifier Dashboard Screen

#### AppBar
- Title: "Verification Queue"
- Role badge: "Verifier" chip (indigo)

#### Metrics (2×2 grid)
- Pending Review count
- In Review count
- Approved This Month
- Average MRV Score

#### Task Queue (ListView)
Each task card:
- Project name + Developer name
- Status badge
- Submitted date + Due date + countdown ("X days remaining" — red if ≤ 3)
- MRV Score (or "Not scored")
- Documents count
- "Review" button → ReviewBottomSheet
- "Approve" / "Reject" buttons (In Review only)

#### Review Bottom Sheet
- Project summary
- MRV data table
- Slider: MRV Score 0–100
- CheckboxListTile:
  - Satellite data valid
  - AI score above threshold
  - Documentation complete
  - No double-counting risk
- Comments TextField
- Action buttons: Approve (emerald) · Request Changes (amber) · Reject (red)

#### Audit Log (expandable)
- Past decisions: Project · Decision · Date · Score · Comments

---

### 8. Project Owner Dashboard Screen

#### AppBar
- Title: "My Projects"
- FAB: "Submit Project" (emerald)

#### Metrics (2×2 grid)
- Total Tokens Minted
- Tokens Sold
- Total Revenue (IDR)
- Active Projects

#### Project List (ListView)
Each project:
- Status badge: Draft · Under Review · Verified · Rejected
- MRV Status: Pending · In Progress · Completed
- Sell-through LinearProgressIndicator
- Revenue in IDR
- "Update MRV" + "View in Marketplace" buttons

#### MRV Upload Sheet (from "Update MRV")
Fields:
- Period (DropdownButton: "2024-Q1" format)
- GPS Coordinates (TextField, accepts JSON array)
- Satellite Photo Link (TextField, URL)
- Estimated CO₂e (NumberField)
- Notes (multiline TextField)
- "Upload Documents" mock button
- "Submit MRV Report" → status → "Under Review"

#### Submit New Project Sheet (from FAB)
Fields:
- Project Name (TextField)
- Category (DropdownButton: Forest/Mangrove/Renewable Energy/Blue Carbon/Peatland)
- Province (DropdownButton)
- Location Name (TextField)
- Latitude / Longitude (NumberField)
- Land Area in hectares (NumberField)
- Description (multiline TextField)
- "Submit Project" → status "draft" → "submitted"

---

### 9. Admin Screen

#### AppBar
- Title: "Admin Panel"
- Role badge: "Admin" (slate)

#### KYC Queue (ListView)
Each user pending KYC:
- User name + email
- KYC Status chip: `unverified` · `pending` · `verified` · `rejected`
- Submitted date
- Documents count
- "Approve KYC" + "Reject" buttons

#### User Management Tab
- Search users
- View user details
- Change role

---

## Data Models (Dart)

```dart
// lib/models/user.dart
class UserModel {
  final int idUser;
  final String namaUser;
  final String email;
  final String statusKyc;       // unverified | pending | verified | rejected
  final String roleName;        // project_owner | investor | verifier | admin
  final String? noHp;
  final DateTime createdAt;
}

// lib/models/wallet.dart
class WalletModel {
  final int idWallet;
  final int idUser;
  final String walletAddress;   // "0x742d355Cc6634C853925a3b944fc9ef13a"
  final String chainNetwork;    // "ethereum" (mock)
  final DateTime createdAt;
}

// lib/models/carbon_project.dart
class CarbonProject {
  final int idProject;
  final int idUser;             // Project owner
  final int idKategori;
  final String namaProject;
  final String lokasi;
  final double? koordinatLat;
  final double? koordinatLng;
  final double luasLahan;       // hectares
  final String? deskripsi;
  final String statusProject;   // draft | submitted | verified | rejected
  final DateTime createdAt;
  final DateTime? updatedAt;
  // Derived/joined fields:
  final String namaKategori;   // from project_categories join
}

// lib/models/mrv_report.dart
class MrvReport {
  final int idMrv;
  final int idProject;
  final int submittedBy;
  final String periodeMrv;      // "2024-Q1"
  final String? koordinatGps;   // JSON array
  final String? linkFotoSatelit;
  final double? estimasiCo2e;
  final String? catatan;
  final String statusMrv;       // submitted | under_review | reviewed | revision_needed
  final DateTime createdAt;
}

// lib/models/verification.dart
class VerificationModel {
  final int idVerifikasi;
  final int idMrv;
  final int idVerifier;
  final String hasil;           // approved | rejected | revision_needed
  final double? volumeCo2eDisetujui;
  final String? catatanAudit;
  final DateTime verifiedAt;
}

// lib/models/carbon_token.dart
class CarbonToken {
  final int idToken;
  final int idProject;
  final int idVerifikasi;
  final int ownerUserId;
  final String tokenSerial;     // "NC-2024-001-000001"
  final int vintageYear;
  final String statusToken;     // available | listed | sold | retired
  final String? txMintHash;     // blockchain tx hash
  final String? metadataHash;
  final DateTime createdAt;
  // Derived fields:
  final String namaProject;
  final String lokasi;
  final String namaKategori;
}

// lib/models/listing.dart
class Listing {
  final int idListing;
  final int idUser;             // Seller
  final int idProject;
  final double hargaPerToken;   // IDR
  final int jumlahToken;
  final String statusListing;   // active | soldout | closed
  final DateTime createdAt;
  // Derived:
  final String namaProject;
  final String sellerName;
}

// lib/models/trade_transaction.dart
class TradeTransaction {
  final int idTransaksi;
  final int idListing;
  final int buyerUserId;
  final int sellerUserId;
  final double totalHarga;      // IDR
  final String metodeBayar;     // crypto | transfer_bank
  final String status;          // pending | paid | failed | success
  final String? txTransferHash;
  final DateTime tanggalTransaksi;
}

// lib/models/retirement.dart
class Retirement {
  final int idRetirement;
  final int idUser;
  final double totalCo2e;
  final String? alasan;         // CSR, regulasi, dll
  final String? namaEntitas;    // Company/individual name on certificate
  final String status;          // pending | completed | failed
  final DateTime createdAt;
}

// lib/models/certificate.dart
class Certificate {
  final int idSertifikat;
  final int idRetirement;
  final String nomorSertifikat; // "CERT-NC-2024-001"
  final String namaEntitas;
  final double totalCo2e;
  final String? linkFilePdf;
  final String? nftTokenId;
  final DateTime createdAt;
}

// lib/models/blockchain_tx.dart
class BlockchainTx {
  final String hash;            // Full SHA-256 hash
  final String previousHash;    // Chain linking
  final String timestamp;
  final String type;            // mint | transfer | retire
  final double amount;          // tCO₂e
  final String? fromAddress;
  final String? toAddress;
  final int blockNumber;
  final double gasFeeMock;      // e.g., 0.004 (ETH, for display only)
}
```

---

## Physical Data Model (15 Tables — MySQL)

### A. Users & Auth

**1. roles**
| Column | Type | Constraint |
|---|---|---|
| id_role | INT AUTO_INCREMENT | PK |
| role_name | VARCHAR(50) | NOT NULL UNIQUE |
| description | TEXT | NULLABLE |

Values: `project_owner`, `investor`, `verifier`, `admin`

**2. users**
| Column | Type | Constraint |
|---|---|---|
| id_user | INT AUTO_INCREMENT | PK |
| nama_user | VARCHAR(150) | NOT NULL |
| email | VARCHAR(255) | NOT NULL UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| no_hp | VARCHAR(20) | NULLABLE |
| status_kyc | ENUM('unverified','pending','verified','rejected') | DEFAULT 'unverified' |
| id_role | INT | FK → roles.id_role |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**3. wallets**
| Column | Type | Constraint |
|---|---|---|
| id_wallet | INT AUTO_INCREMENT | PK |
| id_user | INT UNIQUE | FK → users.id_user |
| wallet_address | VARCHAR(255) | NOT NULL UNIQUE |
| chain_network | VARCHAR(50) | DEFAULT 'ethereum' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

### B. Projects & Documents

**4. project_categories**
| Column | Type | Constraint |
|---|---|---|
| id_kategori | INT AUTO_INCREMENT | PK |
| nama_kategori | VARCHAR(100) | NOT NULL UNIQUE |
| deskripsi | TEXT | NULLABLE |

Values: `Hutan`, `Mangrove`, `Energi Terbarukan`, `Blue Carbon`, `Lahan Gambut`

**5. projects**
| Column | Type | Constraint |
|---|---|---|
| id_project | INT AUTO_INCREMENT | PK |
| id_user | INT | FK → users.id_user |
| id_kategori | INT | FK → project_categories.id_kategori |
| nama_project | VARCHAR(200) | NOT NULL |
| lokasi | VARCHAR(255) | NOT NULL |
| koordinat_lat | DECIMAL(10,7) | NULLABLE |
| koordinat_lng | DECIMAL(10,7) | NULLABLE |
| luas_lahan | DECIMAL(12,2) | NOT NULL (hektar) |
| deskripsi | TEXT | NULLABLE |
| status_project | ENUM('draft','submitted','verified','rejected') | DEFAULT 'draft' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP |

**6. project_documents**
| Column | Type | Constraint |
|---|---|---|
| id_dokumen | INT AUTO_INCREMENT | PK |
| id_project | INT | FK → projects.id_project |
| uploaded_by | INT | FK → users.id_user |
| tipe_dokumen | ENUM | sertifikat_lahan, foto_lokasi, polygon_map, izin_usaha, laporan_teknis |
| file_path | VARCHAR(500) | NOT NULL |
| status_verifikasi | ENUM('pending','approved','rejected') | DEFAULT 'pending' |
| catatan_verifikasi | TEXT | NULLABLE |
| verified_at | TIMESTAMP | NULLABLE |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

### C. MRV & Verifikasi

**7. mrv_reports**
| Column | Type | Constraint |
|---|---|---|
| id_mrv | INT AUTO_INCREMENT | PK |
| id_project | INT | FK → projects.id_project |
| submitted_by | INT | FK → users.id_user |
| periode_mrv | VARCHAR(50) | NOT NULL (e.g., '2024-Q1') |
| koordinat_gps | TEXT | NULLABLE (JSON array) |
| link_foto_satelit | VARCHAR(500) | NULLABLE |
| estimasi_co2e | DECIMAL(14,4) | NULLABLE |
| catatan | TEXT | NULLABLE |
| status_mrv | ENUM('submitted','under_review','reviewed','revision_needed') | DEFAULT 'submitted' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**8. verifications**
| Column | Type | Constraint |
|---|---|---|
| id_verifikasi | INT AUTO_INCREMENT | PK |
| id_mrv | INT | FK → mrv_reports.id_mrv |
| id_verifier | INT | FK → users.id_user (role=verifier) |
| hasil | ENUM('approved','rejected','revision_needed') | NOT NULL |
| volume_co2e_disetujui | DECIMAL(14,4) | NULLABLE |
| catatan_audit | TEXT | NULLABLE |
| verified_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

### D. Tokenisasi

**9. carbon_tokens**
⚠️ Setiap baris = 1 unit token (1 tCO₂e). Status berubah sepanjang lifecycle.

| Column | Type | Constraint |
|---|---|---|
| id_token | INT AUTO_INCREMENT | PK |
| id_project | INT | FK → projects.id_project |
| id_verifikasi | INT | FK → verifications.id_verifikasi |
| owner_user_id | INT | FK → users.id_user |
| token_serial | VARCHAR(100) UNIQUE | NOT NULL (Format: NC-2024-{project}-{seq}) |
| vintage_year | YEAR | NOT NULL |
| status_token | ENUM('available','listed','sold','retired') | DEFAULT 'available' |
| tx_mint_hash | VARCHAR(255) | NULLABLE |
| metadata_hash | VARCHAR(255) | NULLABLE |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

### E. Secondary Market

**10. listings**
| Column | Type | Constraint |
|---|---|---|
| id_listing | INT AUTO_INCREMENT | PK |
| id_user | INT | FK → users.id_user (Seller) |
| id_project | INT | FK → projects.id_project |
| harga_per_token | DECIMAL(14,2) | NOT NULL (IDR) |
| jumlah_token | INT | NOT NULL |
| status_listing | ENUM('active','soldout','closed') | DEFAULT 'active' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**11. trade_transactions**
| Column | Type | Constraint |
|---|---|---|
| id_transaksi | INT AUTO_INCREMENT | PK |
| id_listing | INT | FK → listings.id_listing |
| buyer_user_id | INT | FK → users.id_user |
| seller_user_id | INT | FK → users.id_user (denorm.) |
| total_harga | DECIMAL(16,2) | NOT NULL (IDR) |
| metode_bayar | VARCHAR(50) | NOT NULL |
| status | ENUM('pending','paid','failed','success') | DEFAULT 'pending' |
| tx_transfer_hash | VARCHAR(255) | NULLABLE |
| tanggal_transaksi | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**12. trade_details**
⚠️ 1 transaksi bisa beli banyak token

| Column | Type | Constraint |
|---|---|---|
| id_detail | INT AUTO_INCREMENT | PK |
| id_transaksi | INT | FK → trade_transactions.id_transaksi |
| id_token | INT | FK → carbon_tokens.id_token |
| harga_token | DECIMAL(14,2) | NOT NULL (snapshot saat transaksi) |

---

### F. Retirement & Sertifikasi

**13. retirements**
| Column | Type | Constraint |
|---|---|---|
| id_retirement | INT AUTO_INCREMENT | PK |
| id_user | INT | FK → users.id_user |
| total_co2e | DECIMAL(14,4) | NOT NULL |
| alasan | TEXT | NULLABLE |
| nama_entitas | VARCHAR(200) | NULLABLE |
| status | ENUM('pending','completed','failed') | DEFAULT 'pending' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**14. retirement_details**
| Column | Type | Constraint |
|---|---|---|
| id_detail_retirement | INT AUTO_INCREMENT | PK |
| id_retirement | INT | FK → retirements.id_retirement |
| id_token | INT | FK → carbon_tokens.id_token |
| retired_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**15. certificates**
| Column | Type | Constraint |
|---|---|---|
| id_sertifikat | INT AUTO_INCREMENT | PK |
| id_retirement | INT UNIQUE | FK → retirements.id_retirement |
| nomor_sertifikat | VARCHAR(100) UNIQUE | NOT NULL (CERT-NC-{YEAR}-{SEQ}) |
| nama_entitas | VARCHAR(200) | NOT NULL |
| total_co2e | DECIMAL(14,4) | NOT NULL |
| link_file_pdf | VARCHAR(500) | NULLABLE |
| nft_token_id | VARCHAR(255) | NULLABLE |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

### ⚠️ Blockchain Ledger Table (append-only, not in original proposal — add this)
```sql
CREATE TABLE blockchain_ledger (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  block_number INT NOT NULL,
  tx_hash      VARCHAR(66) NOT NULL UNIQUE,
  prev_hash    VARCHAR(66) NOT NULL,
  tx_type      ENUM('mint','transfer','retire') NOT NULL,
  ref_id       INT NOT NULL,             -- id_token or id_transaksi or id_retirement
  ref_table    VARCHAR(50) NOT NULL,     -- 'carbon_tokens' | 'trade_transactions' | 'retirements'
  amount_co2e  DECIMAL(14,4) NOT NULL,
  from_address VARCHAR(100),
  to_address   VARCHAR(100),
  gas_fee_mock DECIMAL(8,6) DEFAULT 0.004,
  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  -- NO UPDATE, NO DELETE allowed — append only
);
```

---

## Blockchain Simulation (Dart)

```dart
// lib/services/blockchain_service.dart
import 'package:crypto/crypto.dart';
import 'dart:convert';

class BlockchainService {
  static const String genesisHash =
      '0x0000000000000000000000000000000000000000000000000000000000000000';

  // Generate a deterministic SHA-256 transaction hash
  static String generateTxHash({
    required String previousHash,
    required String type,        // mint | transfer | retire
    required double amount,
    required int refId,
    required String timestamp,
  }) {
    final input = '$previousHash|$type|$amount|$refId|$timestamp';
    final bytes = utf8.encode(input);
    final digest = sha256.convert(bytes);
    return '0x${digest.toString()}';
  }

  // Truncate for display: "0x742d...8f3a"
  static String truncateHash(String hash) {
    if (hash.length < 12) return hash;
    return '${hash.substring(0, 6)}...${hash.substring(hash.length - 4)}';
  }

  // Generate mock gas fee (0.003 – 0.007 ETH)
  static double mockGasFee() {
    final fees = [0.003, 0.004, 0.005, 0.006, 0.007];
    return fees[DateTime.now().millisecond % fees.length];
  }
}
```

---

## File Structure

```
lib/
├── main.dart
├── router.dart
├── theme/
│   └── app_theme.dart
├── constants/
│   └── app_colors.dart
├── models/
│   ├── user_model.dart
│   ├── wallet_model.dart
│   ├── carbon_project.dart
│   ├── mrv_report.dart
│   ├── verification_model.dart
│   ├── carbon_token.dart
│   ├── listing.dart
│   ├── trade_transaction.dart
│   ├── retirement.dart
│   ├── certificate.dart
│   └── blockchain_tx.dart
├── data/
│   └── mock_data.dart           # All mock data during Week 1-5
├── services/
│   ├── api_service.dart         # Dio client → Spring Boot REST API
│   ├── blockchain_service.dart  # SHA-256 simulation
│   └── auth_service.dart        # Role + SharedPreferences
├── providers/
│   ├── auth_provider.dart
│   ├── home_provider.dart
│   ├── tokens_provider.dart
│   ├── wallet_provider.dart
│   ├── marketplace_provider.dart
│   ├── owner_provider.dart
│   └── verifier_provider.dart
├── screens/
│   ├── splash_screen.dart
│   ├── home_screen.dart
│   ├── tokens_screen.dart
│   ├── token_detail_screen.dart
│   ├── wallet_screen.dart
│   ├── profile_screen.dart
│   ├── marketplace_screen.dart
│   ├── project_detail_screen.dart
│   ├── verifier_dashboard_screen.dart
│   ├── owner_dashboard_screen.dart
│   └── admin_screen.dart
└── widgets/
    ├── token_card.dart
    ├── project_card.dart
    ├── blockchain_tx_tile.dart
    ├── metric_card.dart
    ├── portfolio_hero_card.dart
    ├── mrv_chart.dart
    ├── portfolio_pie_chart.dart
    ├── price_chart_widget.dart
    ├── buy_token_widget.dart
    ├── review_bottom_sheet.dart
    ├── mrv_upload_sheet.dart
    └── status_badge.dart
```

---

## REST API Endpoints (Spring Boot reference)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/projects` | List all projects (filter by status/kategori) |
| GET | `/api/projects/{id}` | Project detail + MRV data |
| POST | `/api/projects` | Submit new project (Owner) |
| GET | `/api/tokens` | List tokens (filter by owner/status/vintage) |
| GET | `/api/tokens/{id}` | Single token detail |
| GET | `/api/listings` | Marketplace listings (active only) |
| POST | `/api/transactions/buy` | Create trade transaction |
| GET | `/api/transactions/{userId}` | User's transaction history |
| POST | `/api/retirements` | Initiate retirement |
| GET | `/api/retirements/{userId}` | User's retirements |
| GET | `/api/certificates/{retirementId}` | Get certificate |
| GET | `/api/blockchain/ledger/{projectId}` | Blockchain ledger for project |
| POST | `/api/mrv/submit` | Submit MRV report (Owner) |
| PUT | `/api/verifications/{mrvId}` | Submit verification decision (Verifier) |
| GET | `/api/wallet/{userId}` | Wallet info + balance |

---

## Mock Data Summary

### Projects (Mock, 5 data)
| ID | Name | Lokasi | Kategori | Status |
|---|---|---|---|---|
| 1 | Mangrove Restoration Borneo | Kalimantan | Mangrove | Verified |
| 2 | Solar Farm Bali | Bali | Energi Terbarukan | Verified |
| 3 | Rainforest Conservation | Sumatra | Hutan | Verified |
| 4 | Wind Farm Java | Jawa | Energi Terbarukan | Verified |
| 5 | Leuser Ecosystem | Aceh | Hutan | Under Review |

### Token Price Reference
- Base price: **Rp 5,000 per tCO₂e**
- Portfolio value displayed in IDR: `Rp 1,248,500,000`

### Mock User (Buyer)
- Company: PT Carbon Indonesia
- Wallet: `0x742d355Cc6634C853925a3b944fc9ef13a`
- Total Tokens: 23,150 tCO₂e
- Active Projects: 2 (+1 pending)
- KYC Status: Verified

---

## Token Serial & Certificate Naming

```
Token Serial:    NC-{YEAR}-{PROJECT_ID}-{SEQ_6DIGIT}
                 e.g. NC-2024-001-000001

Certificate:     CERT-NC-{YEAR}-{SEQ_3DIGIT}
                 e.g. CERT-NC-2024-001

Transaction Hash: 0x{sha256_full}  → displayed as 0x742d...8f3a
```

---

## PMOB Timeline Alignment

| Minggu | PMOB Target | NusaCarbon Deliverable |
|---|---|---|
| 2 | SRS + ERD + DB Schema | ERD 15 tabel + blockchain_ledger + SRS singkat |
| 3 | REST API CRUD Master Data | Spring Boot: /projects, /tokens, /listings (CRUD) |
| 4 | REST API Modul Transaksi | /transactions/buy, /retirements, /blockchain/ledger |
| 5 | Flutter Setup + UI Dasar | Splash, HomeScreen, bottom nav, AppTheme, mock data |
| 6 | Integrasi API + State (Master) | Provider + Dio connect ke Spring Boot (TokensScreen) |
| 7 | Modul Transaksi (Input) | Buy flow: listing selection → quantity → price calc |
| 8 | Checkout + History | Checkout → MySQL → blockchain_ledger entry → WalletScreen tx list |
| 9 | Laporan Sederhana | HomeScreen portfolio chart, fl_chart price line, retirement history |
| 10 | State Lanjutan + Validasi | Form validation, loading states, error handling |
| 11 | UI/UX Polish | ThemeData complete, animations, consistent spacing |
| 12 | Testing | Regression test all flows, edge cases |
| 13 | Build APK + Docs | flutter build apk --release, User Manual |
| 14 | Presentasi Final | Demo end-to-end: Register → MRV → Verify → Mint → Buy → Retire |

---

## Core Constraints

1. **Mock data only during development** (Week 1–5) — Real API from Week 6+
2. **No real payments** — "Buy Tokens" triggers mock success BottomSheet + generated hash
3. **No real blockchain** — SHA-256 simulation, append-only MySQL table
4. **1 token = 1 tCO₂e** — Always show equivalency when displaying token quantities
5. **Currency: IDR** — All monetary values in Rupiah (`Rp X,XXX,XXX`)
6. **Gas fees: mock ETH** — Show for realism only, not real values
7. **Hashes always truncated** for display: `0x742d...8f3a` (monospace font)
8. **KYC status** must show in Profile — all roles have KYC requirements
9. **Blockchain ledger is append-only** — No DELETE/UPDATE in `blockchain_ledger` table
10. **retirement = token burned** — Once retired, `status_token` → 'retired', immutable

---

## Summary

NusaCarbon adalah Flutter mobile app dengan backend Spring Boot dan database MySQL yang mengimplementasikan marketplace token kredit karbon berbasis simulasi blockchain untuk Indonesia. Empat aktor (Project Owner, Verifier, Buyer, Admin) menjalankan lifecycle penuh: Owner submit proyek + MRV → Verifier setujui → Token di-mint → Buyer beli token di marketplace → Buyer retire token → Sertifikat digital terbit. Blockchain disimulasikan dengan SHA-256 chain-linked hashes di tabel append-only. Semua harga dalam IDR (Rp 5.000 per tCO₂e base price). UI mengikuti desain Figma dengan bottom nav: Home · Tokens · Wallet · Profile.
