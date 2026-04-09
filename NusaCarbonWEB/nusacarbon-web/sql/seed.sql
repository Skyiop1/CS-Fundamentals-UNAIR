-- Roles
INSERT INTO roles (role_name) VALUES ('buyer'), ('owner'), ('verifier'), ('admin');

-- Mock Users (password = bcrypt of "password123")
INSERT INTO users (nama_user, email, password, status_kyc, id_role) VALUES
('PT Carbon Indonesia', 'buyer@nusacarbon.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'verified', 1),
('Yayasan Hutan Lestari', 'owner@nusacarbon.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'verified', 2),
('Dr. Aulia Verifikator', 'verifier@nusacarbon.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'verified', 3),
('Admin NusaCarbon', 'admin@nusacarbon.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'verified', 4);

-- Mock Wallets
INSERT INTO wallets (id_user, wallet_address, saldo_token) VALUES
(1, '0x742d355Cc6634C853925a3b944fc9ef13a', 23150),
(2, '0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e', 0);

-- Project Categories
INSERT INTO project_categories (nama_kategori) VALUES
('Hutan'), ('Mangrove'), ('Energi Terbarukan'), ('Blue Carbon'), ('Lahan Gambut');

-- Mock Projects (5 data)
INSERT INTO projects (id_user, id_kategori, nama_project, lokasi, luas_lahan, deskripsi, status_project) VALUES
(2, 2, 'Mangrove Restoration Borneo', 'Kalimantan Barat', 15000.00, 'Restorasi mangrove di pesisir Kalimantan Barat untuk penyerapan karbon dan perlindungan ekosistem pesisir.', 'verified'),
(2, 3, 'Solar Farm Bali', 'Bali', 500.00, 'Pembangkit listrik tenaga surya skala besar di Bali sebagai alternatif energi bersih.', 'verified'),
(2, 1, 'Rainforest Conservation Sumatra', 'Sumatera Barat', 45000.00, 'Konservasi hutan hujan tropis Sumatera untuk melindungi biodiversitas dan menyerap karbon.', 'verified'),
(2, 3, 'Wind Farm Java', 'Jawa Tengah', 800.00, 'Pembangkit listrik tenaga angin di Jawa Tengah untuk pengurangan emisi energi fosil.', 'verified'),
(2, 1, 'Leuser Ecosystem', 'Aceh', 62000.00, 'Perlindungan ekosistem Leuser di Aceh, habitat orangutan dan harimau Sumatera.', 'submitted');

-- We also insert some mock listings to display correctly in the marketplace.
-- Base price: Rp 5.000 per tCO₂e. 
-- Listing 1: Mangrove Restoration Borneo
INSERT INTO listings (id_user, id_project, harga_per_token, jumlah_token, status_listing) VALUES
(2, 1, 5000.00, 10000, 'active'),
(2, 2, 5000.00, 5000, 'active'),
(2, 3, 5000.00, 20000, 'active'),
(2, 4, 5000.00, 15000, 'active');
