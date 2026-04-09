-- ROLES
CREATE TABLE roles (
  id_role INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(50) NOT NULL UNIQUE
);

-- USERS
CREATE TABLE users (
  id_user INT AUTO_INCREMENT PRIMARY KEY,
  nama_user VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,  -- bcrypt hash
  no_hp VARCHAR(20),
  status_kyc ENUM('unverified','pending','verified','rejected') DEFAULT 'unverified',
  id_role INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_role) REFERENCES roles(id_role)
);

-- WALLETS
CREATE TABLE wallets (
  id_wallet INT AUTO_INCREMENT PRIMARY KEY,
  id_user INT NOT NULL UNIQUE,
  wallet_address VARCHAR(100) NOT NULL,
  saldo_token DECIMAL(14,4) DEFAULT 0,
  FOREIGN KEY (id_user) REFERENCES users(id_user)
);

-- PROJECT CATEGORIES
CREATE TABLE project_categories (
  id_kategori INT AUTO_INCREMENT PRIMARY KEY,
  nama_kategori VARCHAR(100) NOT NULL,
  deskripsi TEXT
);

-- PROJECTS
CREATE TABLE projects (
  id_project INT AUTO_INCREMENT PRIMARY KEY,
  id_user INT NOT NULL,
  id_kategori INT NOT NULL,
  nama_project VARCHAR(200) NOT NULL,
  lokasi VARCHAR(200),
  luas_lahan DECIMAL(10,2),
  deskripsi TEXT,
  status_project ENUM('draft','submitted','verified','rejected') DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id_user),
  FOREIGN KEY (id_kategori) REFERENCES project_categories(id_kategori)
);

-- PROJECT DOCUMENTS
CREATE TABLE project_documents (
  id_dokumen INT AUTO_INCREMENT PRIMARY KEY,
  id_project INT NOT NULL,
  tipe_dokumen ENUM('sertifikat_lahan','foto_lokasi','polygon_map','izin_usaha','laporan_teknis') NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  uploaded_by INT NOT NULL,
  status_verifikasi ENUM('pending','approved','rejected') DEFAULT 'pending',
  catatan_verifikasi TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  verified_at TIMESTAMP NULL,
  FOREIGN KEY (id_project) REFERENCES projects(id_project),
  FOREIGN KEY (uploaded_by) REFERENCES users(id_user)
);

-- MRV REPORTS
CREATE TABLE mrv_reports (
  id_mrv INT AUTO_INCREMENT PRIMARY KEY,
  id_project INT NOT NULL,
  periode_mrv VARCHAR(20) NOT NULL,  -- e.g. "Q1 2025"
  koordinat_gps VARCHAR(100),
  link_foto_satelit VARCHAR(500),
  catatan TEXT,
  status_mrv ENUM('submitted','reviewed') DEFAULT 'submitted',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_project) REFERENCES projects(id_project)
);

-- VERIFICATIONS
CREATE TABLE verifications (
  id_verifikasi INT AUTO_INCREMENT PRIMARY KEY,
  id_mrv INT NOT NULL,
  id_verifier INT NOT NULL,
  hasil ENUM('approve','reject','revisi') NOT NULL,
  volume_co2e_disetujui DECIMAL(14,4),
  catatan_audit TEXT,
  verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_mrv) REFERENCES mrv_reports(id_mrv),
  FOREIGN KEY (id_verifier) REFERENCES users(id_user)
);

-- CARBON TOKENS
CREATE TABLE carbon_tokens (
  id_token INT AUTO_INCREMENT PRIMARY KEY,
  id_project INT NOT NULL,
  token_serial VARCHAR(50) NOT NULL UNIQUE,  -- e.g. NC-2024-001-000001
  vintage_year YEAR NOT NULL,
  status_token ENUM('available','listed','sold','retired') DEFAULT 'available',
  owner_user_id INT NOT NULL,
  tx_mint_hash VARCHAR(66),
  metadata_hash VARCHAR(66),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_project) REFERENCES projects(id_project),
  FOREIGN KEY (owner_user_id) REFERENCES users(id_user)
);

-- LISTINGS
CREATE TABLE listings (
  id_listing INT AUTO_INCREMENT PRIMARY KEY,
  id_user INT NOT NULL,
  id_project INT NOT NULL,
  harga_per_token DECIMAL(12,2) NOT NULL,
  jumlah_token INT NOT NULL,
  status_listing ENUM('active','soldout','closed') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id_user),
  FOREIGN KEY (id_project) REFERENCES projects(id_project)
);

-- TRADE TRANSACTIONS
CREATE TABLE trade_transactions (
  id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
  id_listing INT NOT NULL,
  buyer_user_id INT NOT NULL,
  seller_user_id INT NOT NULL,
  total_harga DECIMAL(16,2) NOT NULL,
  metode_bayar VARCHAR(50) DEFAULT 'mock_payment',
  status ENUM('pending','paid','failed','success') DEFAULT 'pending',
  tx_transfer_hash VARCHAR(66),
  tanggal_transaksi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_listing) REFERENCES listings(id_listing),
  FOREIGN KEY (buyer_user_id) REFERENCES users(id_user),
  FOREIGN KEY (seller_user_id) REFERENCES users(id_user)
);

-- TRADE DETAILS
CREATE TABLE trade_details (
  id_detail_transaksi INT AUTO_INCREMENT PRIMARY KEY,
  id_transaksi INT NOT NULL,
  id_token INT NOT NULL,
  harga_token DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (id_transaksi) REFERENCES trade_transactions(id_transaksi),
  FOREIGN KEY (id_token) REFERENCES carbon_tokens(id_token)
);

-- RETIREMENTS
CREATE TABLE retirements (
  id_retirement INT AUTO_INCREMENT PRIMARY KEY,
  id_user INT NOT NULL,
  nama_entitas VARCHAR(200),
  total_co2e DECIMAL(14,4) NOT NULL,
  tx_retirement_hash VARCHAR(66),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id_user)
);

-- RETIREMENT DETAILS
CREATE TABLE retirement_details (
  id_detail_retirement INT AUTO_INCREMENT PRIMARY KEY,
  id_retirement INT NOT NULL,
  id_token INT NOT NULL,
  FOREIGN KEY (id_retirement) REFERENCES retirements(id_retirement),
  FOREIGN KEY (id_token) REFERENCES carbon_tokens(id_token)
);

-- CERTIFICATES
CREATE TABLE certificates (
  id_sertifikat INT AUTO_INCREMENT PRIMARY KEY,
  id_retirement INT NOT NULL,
  nomor_sertifikat VARCHAR(50) NOT NULL UNIQUE,  -- e.g. CERT-NC-2025-001
  nama_entitas VARCHAR(200),
  total_co2e DECIMAL(14,4) NOT NULL,
  link_file_pdf VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_retirement) REFERENCES retirements(id_retirement)
);

-- BLOCKCHAIN LEDGER (APPEND-ONLY — NO UPDATE, NO DELETE)
CREATE TABLE blockchain_ledger (
  id INT AUTO_INCREMENT PRIMARY KEY,
  block_number INT NOT NULL,
  tx_hash VARCHAR(66) NOT NULL UNIQUE,
  prev_hash VARCHAR(66) NOT NULL,
  tx_type ENUM('mint','transfer','retire') NOT NULL,
  ref_id INT NOT NULL,
  ref_table VARCHAR(50) NOT NULL,
  amount_co2e DECIMAL(14,4) NOT NULL,
  from_address VARCHAR(100),
  to_address VARCHAR(100),
  gas_fee_mock DECIMAL(8,6) DEFAULT 0.004,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
