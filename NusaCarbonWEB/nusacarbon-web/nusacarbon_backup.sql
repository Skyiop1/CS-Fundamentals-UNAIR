-- MySQL dump 10.13  Distrib 8.0.45, for Linux (aarch64)
--
-- Host: localhost    Database: nusacarbon
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blockchain_ledger`
--

DROP TABLE IF EXISTS `blockchain_ledger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blockchain_ledger` (
  `id` int NOT NULL AUTO_INCREMENT,
  `block_number` int NOT NULL,
  `tx_hash` varchar(66) NOT NULL,
  `prev_hash` varchar(66) NOT NULL,
  `tx_type` enum('mint','transfer','retire') NOT NULL,
  `ref_id` int NOT NULL,
  `ref_table` varchar(50) NOT NULL,
  `amount_co2e` decimal(14,4) NOT NULL,
  `from_address` varchar(100) DEFAULT NULL,
  `to_address` varchar(100) DEFAULT NULL,
  `gas_fee_mock` decimal(8,6) DEFAULT '0.004000',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tx_hash` (`tx_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blockchain_ledger`
--

LOCK TABLES `blockchain_ledger` WRITE;
/*!40000 ALTER TABLE `blockchain_ledger` DISABLE KEYS */;
/*!40000 ALTER TABLE `blockchain_ledger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carbon_tokens`
--

DROP TABLE IF EXISTS `carbon_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carbon_tokens` (
  `id_token` int NOT NULL AUTO_INCREMENT,
  `id_project` int NOT NULL,
  `token_serial` varchar(50) NOT NULL,
  `vintage_year` year NOT NULL,
  `status_token` enum('available','listed','sold','retired') DEFAULT 'available',
  `owner_user_id` int NOT NULL,
  `tx_mint_hash` varchar(66) DEFAULT NULL,
  `metadata_hash` varchar(66) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_token`),
  UNIQUE KEY `token_serial` (`token_serial`),
  KEY `id_project` (`id_project`),
  KEY `owner_user_id` (`owner_user_id`),
  CONSTRAINT `carbon_tokens_ibfk_1` FOREIGN KEY (`id_project`) REFERENCES `projects` (`id_project`),
  CONSTRAINT `carbon_tokens_ibfk_2` FOREIGN KEY (`owner_user_id`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carbon_tokens`
--

LOCK TABLES `carbon_tokens` WRITE;
/*!40000 ALTER TABLE `carbon_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `carbon_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `id_sertifikat` int NOT NULL AUTO_INCREMENT,
  `id_retirement` int NOT NULL,
  `nomor_sertifikat` varchar(50) NOT NULL,
  `nama_entitas` varchar(200) DEFAULT NULL,
  `total_co2e` decimal(14,4) NOT NULL,
  `link_file_pdf` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_sertifikat`),
  UNIQUE KEY `nomor_sertifikat` (`nomor_sertifikat`),
  KEY `id_retirement` (`id_retirement`),
  CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`id_retirement`) REFERENCES `retirements` (`id_retirement`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificates`
--

LOCK TABLES `certificates` WRITE;
/*!40000 ALTER TABLE `certificates` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listings`
--

DROP TABLE IF EXISTS `listings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listings` (
  `id_listing` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `id_project` int NOT NULL,
  `harga_per_token` decimal(12,2) NOT NULL,
  `jumlah_token` int NOT NULL,
  `status_listing` enum('active','soldout','closed') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_listing`),
  KEY `id_user` (`id_user`),
  KEY `id_project` (`id_project`),
  CONSTRAINT `listings_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  CONSTRAINT `listings_ibfk_2` FOREIGN KEY (`id_project`) REFERENCES `projects` (`id_project`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listings`
--

LOCK TABLES `listings` WRITE;
/*!40000 ALTER TABLE `listings` DISABLE KEYS */;
INSERT INTO `listings` VALUES (1,2,1,5000.00,10000,'active','2026-04-09 10:14:36'),(2,2,2,5000.00,5000,'active','2026-04-09 10:14:36'),(3,2,3,5000.00,20000,'active','2026-04-09 10:14:36'),(4,2,4,5000.00,15000,'active','2026-04-09 10:14:36');
/*!40000 ALTER TABLE `listings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mrv_reports`
--

DROP TABLE IF EXISTS `mrv_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mrv_reports` (
  `id_mrv` int NOT NULL AUTO_INCREMENT,
  `id_project` int NOT NULL,
  `periode_mrv` varchar(20) NOT NULL,
  `koordinat_gps` varchar(100) DEFAULT NULL,
  `link_foto_satelit` varchar(500) DEFAULT NULL,
  `catatan` text,
  `status_mrv` enum('submitted','reviewed') DEFAULT 'submitted',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_mrv`),
  KEY `id_project` (`id_project`),
  CONSTRAINT `mrv_reports_ibfk_1` FOREIGN KEY (`id_project`) REFERENCES `projects` (`id_project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mrv_reports`
--

LOCK TABLES `mrv_reports` WRITE;
/*!40000 ALTER TABLE `mrv_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `mrv_reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_categories`
--

DROP TABLE IF EXISTS `project_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_categories` (
  `id_kategori` int NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(100) NOT NULL,
  `deskripsi` text,
  PRIMARY KEY (`id_kategori`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_categories`
--

LOCK TABLES `project_categories` WRITE;
/*!40000 ALTER TABLE `project_categories` DISABLE KEYS */;
INSERT INTO `project_categories` VALUES (1,'Hutan',NULL),(2,'Mangrove',NULL),(3,'Energi Terbarukan',NULL),(4,'Blue Carbon',NULL),(5,'Lahan Gambut',NULL);
/*!40000 ALTER TABLE `project_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_documents`
--

DROP TABLE IF EXISTS `project_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_documents` (
  `id_dokumen` int NOT NULL AUTO_INCREMENT,
  `id_project` int NOT NULL,
  `tipe_dokumen` enum('sertifikat_lahan','foto_lokasi','polygon_map','izin_usaha','laporan_teknis') NOT NULL,
  `file_path` varchar(500) NOT NULL,
  `uploaded_by` int NOT NULL,
  `status_verifikasi` enum('pending','approved','rejected') DEFAULT 'pending',
  `catatan_verifikasi` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `verified_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id_dokumen`),
  KEY `id_project` (`id_project`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `project_documents_ibfk_1` FOREIGN KEY (`id_project`) REFERENCES `projects` (`id_project`),
  CONSTRAINT `project_documents_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_documents`
--

LOCK TABLES `project_documents` WRITE;
/*!40000 ALTER TABLE `project_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id_project` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `id_kategori` int NOT NULL,
  `nama_project` varchar(200) NOT NULL,
  `lokasi` varchar(200) DEFAULT NULL,
  `luas_lahan` decimal(10,2) DEFAULT NULL,
  `deskripsi` text,
  `status_project` enum('draft','submitted','verified','rejected') DEFAULT 'draft',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_project`),
  KEY `id_user` (`id_user`),
  KEY `id_kategori` (`id_kategori`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  CONSTRAINT `projects_ibfk_2` FOREIGN KEY (`id_kategori`) REFERENCES `project_categories` (`id_kategori`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,2,2,'Mangrove Restoration Borneo','Kalimantan Barat',15000.00,'Restorasi mangrove di pesisir Kalimantan Barat untuk penyerapan karbon dan perlindungan ekosistem pesisir.','verified','2026-04-09 10:14:36'),(2,2,3,'Solar Farm Bali','Bali',500.00,'Pembangkit listrik tenaga surya skala besar di Bali sebagai alternatif energi bersih.','verified','2026-04-09 10:14:36'),(3,2,1,'Rainforest Conservation Sumatra','Sumatera Barat',45000.00,'Konservasi hutan hujan tropis Sumatera untuk melindungi biodiversitas dan menyerap karbon.','verified','2026-04-09 10:14:36'),(4,2,3,'Wind Farm Java','Jawa Tengah',800.00,'Pembangkit listrik tenaga angin di Jawa Tengah untuk pengurangan emisi energi fosil.','verified','2026-04-09 10:14:36'),(5,2,1,'Leuser Ecosystem','Aceh',62000.00,'Perlindungan ekosistem Leuser di Aceh, habitat orangutan dan harimau Sumatera.','submitted','2026-04-09 10:14:36');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retirement_details`
--

DROP TABLE IF EXISTS `retirement_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retirement_details` (
  `id_detail_retirement` int NOT NULL AUTO_INCREMENT,
  `id_retirement` int NOT NULL,
  `id_token` int NOT NULL,
  PRIMARY KEY (`id_detail_retirement`),
  KEY `id_retirement` (`id_retirement`),
  KEY `id_token` (`id_token`),
  CONSTRAINT `retirement_details_ibfk_1` FOREIGN KEY (`id_retirement`) REFERENCES `retirements` (`id_retirement`),
  CONSTRAINT `retirement_details_ibfk_2` FOREIGN KEY (`id_token`) REFERENCES `carbon_tokens` (`id_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retirement_details`
--

LOCK TABLES `retirement_details` WRITE;
/*!40000 ALTER TABLE `retirement_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `retirement_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retirements`
--

DROP TABLE IF EXISTS `retirements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retirements` (
  `id_retirement` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `nama_entitas` varchar(200) DEFAULT NULL,
  `total_co2e` decimal(14,4) NOT NULL,
  `tx_retirement_hash` varchar(66) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_retirement`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `retirements_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retirements`
--

LOCK TABLES `retirements` WRITE;
/*!40000 ALTER TABLE `retirements` DISABLE KEYS */;
/*!40000 ALTER TABLE `retirements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_role` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id_role`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (4,'admin'),(1,'buyer'),(2,'owner'),(3,'verifier');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_details`
--

DROP TABLE IF EXISTS `trade_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_details` (
  `id_detail_transaksi` int NOT NULL AUTO_INCREMENT,
  `id_transaksi` int NOT NULL,
  `id_token` int NOT NULL,
  `harga_token` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id_detail_transaksi`),
  KEY `id_transaksi` (`id_transaksi`),
  KEY `id_token` (`id_token`),
  CONSTRAINT `trade_details_ibfk_1` FOREIGN KEY (`id_transaksi`) REFERENCES `trade_transactions` (`id_transaksi`),
  CONSTRAINT `trade_details_ibfk_2` FOREIGN KEY (`id_token`) REFERENCES `carbon_tokens` (`id_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_details`
--

LOCK TABLES `trade_details` WRITE;
/*!40000 ALTER TABLE `trade_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `trade_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_transactions`
--

DROP TABLE IF EXISTS `trade_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_transactions` (
  `id_transaksi` int NOT NULL AUTO_INCREMENT,
  `id_listing` int NOT NULL,
  `buyer_user_id` int NOT NULL,
  `seller_user_id` int NOT NULL,
  `total_harga` decimal(16,2) NOT NULL,
  `metode_bayar` varchar(50) DEFAULT 'mock_payment',
  `status` enum('pending','paid','failed','success') DEFAULT 'pending',
  `tx_transfer_hash` varchar(66) DEFAULT NULL,
  `tanggal_transaksi` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_transaksi`),
  KEY `id_listing` (`id_listing`),
  KEY `buyer_user_id` (`buyer_user_id`),
  KEY `seller_user_id` (`seller_user_id`),
  CONSTRAINT `trade_transactions_ibfk_1` FOREIGN KEY (`id_listing`) REFERENCES `listings` (`id_listing`),
  CONSTRAINT `trade_transactions_ibfk_2` FOREIGN KEY (`buyer_user_id`) REFERENCES `users` (`id_user`),
  CONSTRAINT `trade_transactions_ibfk_3` FOREIGN KEY (`seller_user_id`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_transactions`
--

LOCK TABLES `trade_transactions` WRITE;
/*!40000 ALTER TABLE `trade_transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `trade_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `nama_user` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `status_kyc` enum('unverified','pending','verified','rejected') DEFAULT 'unverified',
  `id_role` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `email` (`email`),
  KEY `id_role` (`id_role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'PT Carbon Indonesia','buyer@nusacarbon.id','$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',NULL,'verified',1,'2026-04-09 10:14:36'),(2,'Yayasan Hutan Lestari','owner@nusacarbon.id','$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',NULL,'verified',2,'2026-04-09 10:14:36'),(3,'Dr. Aulia Verifikator','verifier@nusacarbon.id','$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',NULL,'verified',3,'2026-04-09 10:14:36'),(4,'Admin NusaCarbon','admin@nusacarbon.id','$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',NULL,'verified',4,'2026-04-09 10:14:36'),(5,'Test User Baru','test@nusacarbon.id','$2y$10$T8k9BZ6hksw6RF7STh17kuO3BF67mW64HlEgBwhtkuGjF78wWYiJm','081234567890','pending',1,'2026-04-09 10:22:14'),(6,'Perusahaan Hijau Test','newacc@test.com','$2y$10$BKQsaE1naX44gh10Bste5OPfZHEL0o6qfX3Sc2SV9gnoF6AfyR63S','081234567890','pending',1,'2026-04-09 10:33:42'),(7,'NaufalZaki','nz@gmail.com','$2y$10$Q3u8RFAXpzM0PS78Ml4raeYOy44ViAVLI8Rq50Hzd33OYcEsxxK3u','+6287733621960','pending',1,'2026-04-09 11:09:22');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verifications`
--

DROP TABLE IF EXISTS `verifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verifications` (
  `id_verifikasi` int NOT NULL AUTO_INCREMENT,
  `id_mrv` int NOT NULL,
  `id_verifier` int NOT NULL,
  `hasil` enum('approve','reject','revisi') NOT NULL,
  `volume_co2e_disetujui` decimal(14,4) DEFAULT NULL,
  `catatan_audit` text,
  `verified_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_verifikasi`),
  KEY `id_mrv` (`id_mrv`),
  KEY `id_verifier` (`id_verifier`),
  CONSTRAINT `verifications_ibfk_1` FOREIGN KEY (`id_mrv`) REFERENCES `mrv_reports` (`id_mrv`),
  CONSTRAINT `verifications_ibfk_2` FOREIGN KEY (`id_verifier`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verifications`
--

LOCK TABLES `verifications` WRITE;
/*!40000 ALTER TABLE `verifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `verifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wallets`
--

DROP TABLE IF EXISTS `wallets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallets` (
  `id_wallet` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `wallet_address` varchar(100) NOT NULL,
  `saldo_token` decimal(14,4) DEFAULT '0.0000',
  PRIMARY KEY (`id_wallet`),
  UNIQUE KEY `id_user` (`id_user`),
  CONSTRAINT `wallets_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wallets`
--

LOCK TABLES `wallets` WRITE;
/*!40000 ALTER TABLE `wallets` DISABLE KEYS */;
INSERT INTO `wallets` VALUES (1,1,'0x742d355Cc6634C853925a3b944fc9ef13a',23150.0000),(2,2,'0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e',0.0000),(3,5,'0x66e0f5ce9510ff07a1ef39bbde8eeb035148d0aa',0.0000),(4,6,'0xb2fdfd41f6ef21a84d1ef1e6d1b1d5b9f90f55f7',0.0000),(5,7,'0x1233f467532276b0aa5b4ed71e0ab11ce5240714',0.0000);
/*!40000 ALTER TABLE `wallets` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-09 12:05:20
