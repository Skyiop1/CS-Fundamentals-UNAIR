package com.nusacarbon.api.config;

import com.nusacarbon.api.entity.*;
import com.nusacarbon.api.entity.enums.*;
import com.nusacarbon.api.repository.*;
import com.nusacarbon.api.util.BlockchainHashUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataSeeder implements CommandLineRunner {

    private final RoleRepository roleRepository;
    private final UserRepository userRepository;
    private final WalletRepository walletRepository;
    private final ProjectCategoryRepository categoryRepository;
    private final ProjectRepository projectRepository;
    private final MrvReportRepository mrvReportRepository;
    private final VerificationRepository verificationRepository;
    private final CarbonTokenRepository tokenRepository;
    private final ListingRepository listingRepository;
    private final BlockchainLedgerRepository ledgerRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        if (roleRepository.count() > 0) {
            log.info("Database already seeded. Skipping.");
            return;
        }

        log.info("=== Seeding NusaCarbon database ===");

        // --- ROLES ---
        Role roleOwner = roleRepository.save(Role.builder().roleName("project_owner").description("Pengelola lahan/teknologi hijau").build());
        Role roleInvestor = roleRepository.save(Role.builder().roleName("investor").description("Pembeli token karbon").build());
        Role roleVerifier = roleRepository.save(Role.builder().roleName("verifier").description("Auditor independen").build());
        Role roleAdmin = roleRepository.save(Role.builder().roleName("admin").description("Pengelola platform").build());
        log.info("✓ 4 roles created");

        // --- PROJECT CATEGORIES ---
        ProjectCategory catHutan = categoryRepository.save(ProjectCategory.builder().namaKategori("Hutan").deskripsi("Konservasi dan restorasi hutan alam").build());
        ProjectCategory catMangrove = categoryRepository.save(ProjectCategory.builder().namaKategori("Mangrove").deskripsi("Restorasi ekosistem mangrove").build());
        ProjectCategory catEnergi = categoryRepository.save(ProjectCategory.builder().namaKategori("Energi Terbarukan").deskripsi("Solar, wind, dan energi bersih lainnya").build());
        ProjectCategory catBlueCarbon = categoryRepository.save(ProjectCategory.builder().namaKategori("Blue Carbon").deskripsi("Karbon biru dari ekosistem laut").build());
        ProjectCategory catGambut = categoryRepository.save(ProjectCategory.builder().namaKategori("Lahan Gambut").deskripsi("Restorasi dan perlindungan lahan gambut").build());
        log.info("✓ 5 project categories created");

        // --- USERS ---
        String hashedPw = passwordEncoder.encode("password123");

        User buyer = userRepository.save(User.builder()
                .namaUser("PT Carbon Indonesia").email("carbonpt@nusacarbon.co.id")
                .passwordHash(hashedPw).noHp("081234567890").statusKyc(KycStatus.verified).role(roleInvestor).build());

        User owner = userRepository.save(User.builder()
                .namaUser("PT Hijau Nusantara").email("owner@nusacarbon.co.id")
                .passwordHash(hashedPw).noHp("081234567891").statusKyc(KycStatus.verified).role(roleOwner).build());

        User verifier = userRepository.save(User.builder()
                .namaUser("Badan Verifikasi Nasional").email("verifier@nusacarbon.co.id")
                .passwordHash(hashedPw).noHp("081234567892").statusKyc(KycStatus.verified).role(roleVerifier).build());

        User admin = userRepository.save(User.builder()
                .namaUser("Admin NusaCarbon").email("admin@nusacarbon.co.id")
                .passwordHash(hashedPw).noHp("081234567893").statusKyc(KycStatus.verified).role(roleAdmin).build());

        User owner2 = userRepository.save(User.builder()
                .namaUser("PT Lestari Alam").email("lestari@nusacarbon.co.id")
                .passwordHash(hashedPw).noHp("081234567894").statusKyc(KycStatus.verified).role(roleOwner).build());

        User pendingUser = userRepository.save(User.builder()
                .namaUser("PT Baru Daftar").email("pending@nusacarbon.co.id")
                .passwordHash(hashedPw).statusKyc(KycStatus.pending).role(roleInvestor).build());
        log.info("✓ 6 users created");

        // --- WALLETS ---
        walletRepository.save(Wallet.builder().user(buyer).walletAddress("0x742d355Cc6634C853925a3b944fc9ef13a").chainNetwork("ethereum").idrBalance(new BigDecimal("3000000.00")).build());
        walletRepository.save(Wallet.builder().user(owner).walletAddress("0xA1b2C3d4E5f6789012345678901234567890").chainNetwork("ethereum").build());
        walletRepository.save(Wallet.builder().user(verifier).walletAddress("0xB2c3D4e5F6a7890123456789012345678901").chainNetwork("ethereum").build());
        walletRepository.save(Wallet.builder().user(admin).walletAddress("0xC3d4E5f6A7b8901234567890123456789012").chainNetwork("ethereum").build());
        walletRepository.save(Wallet.builder().user(owner2).walletAddress("0xD4e5F6a7B8c9012345678901234567890123").chainNetwork("ethereum").build());
        log.info("✓ 5 wallets created");

        // --- PROJECTS ---
        Project p1 = projectRepository.save(Project.builder()
                .user(owner).kategori(catMangrove).namaProject("Mangrove Restoration Borneo")
                .lokasi("Kalimantan, Indonesia")
                .koordinatLat(new BigDecimal("-1.2427800")).koordinatLng(new BigDecimal("116.8528700"))
                .luasLahan(new BigDecimal("2500.00"))
                .deskripsi("Restorasi 2.500 hektar ekosistem mangrove di pesisir Kalimantan Selatan untuk sekuestrasi karbon.")
                .imageUrl("https://images.unsplash.com/photo-1573126617899-41f1dffb196c?w=800&q=80")
                .statusProject(ProjectStatus.verified).build());

        Project p2 = projectRepository.save(Project.builder()
                .user(owner2).kategori(catEnergi).namaProject("Solar Farm Bali")
                .lokasi("Bali, Indonesia")
                .koordinatLat(new BigDecimal("-8.3405200")).koordinatLng(new BigDecimal("115.0920000"))
                .luasLahan(new BigDecimal("150.00"))
                .deskripsi("Pembangkit listrik tenaga surya 50MW di Karangasem, Bali untuk menggantikan pembangkit batu bara.")
                .imageUrl("https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800&q=80")
                .statusProject(ProjectStatus.verified).build());

        Project p3 = projectRepository.save(Project.builder()
                .user(owner).kategori(catHutan).namaProject("Rainforest Conservation")
                .lokasi("Sumatra, Indonesia")
                .koordinatLat(new BigDecimal("0.5897000")).koordinatLng(new BigDecimal("101.3431000"))
                .luasLahan(new BigDecimal("10000.00"))
                .deskripsi("Konservasi 10.000 hektar hutan hujan tropis di Riau, Sumatra untuk mencegah deforestasi.")
                .imageUrl("https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&q=80")
                .statusProject(ProjectStatus.verified).build());

        Project p4 = projectRepository.save(Project.builder()
                .user(owner2).kategori(catEnergi).namaProject("Wind Farm Java")
                .lokasi("Jawa, Indonesia")
                .koordinatLat(new BigDecimal("-7.7956000")).koordinatLng(new BigDecimal("110.3695000"))
                .luasLahan(new BigDecimal("800.00"))
                .deskripsi("Pembangkit listrik tenaga angin 30MW di pesisir utara Jawa.")
                .imageUrl("https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=800&q=80")
                .statusProject(ProjectStatus.verified).build());

        Project p5 = projectRepository.save(Project.builder()
                .user(owner).kategori(catHutan).namaProject("Leuser Ecosystem")
                .lokasi("Aceh, Indonesia")
                .koordinatLat(new BigDecimal("3.7000000")).koordinatLng(new BigDecimal("97.5000000"))
                .luasLahan(new BigDecimal("25000.00"))
                .deskripsi("Perlindungan ekosistem Leuser yang merupakan habitat orangutan, harimau dan gajah Sumatra.")
                .imageUrl("https://images.unsplash.com/photo-1511497584788-876760111969?w=800&q=80")
                .statusProject(ProjectStatus.submitted).build());

        Project p6 = projectRepository.save(Project.builder()
                .user(owner).kategori(catHutan).namaProject("Hutan Pinus Sumatera")
                .lokasi("Sumatera, Indonesia")
                .koordinatLat(new BigDecimal("1.5000000")).koordinatLng(new BigDecimal("99.5000000"))
                .luasLahan(new BigDecimal("5000.00"))
                .deskripsi("Perlindungan dan pengelolaan hutan pinus lestari di pegunungan Sumatera.")
                .imageUrl("https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=800&q=80")
                .statusProject(ProjectStatus.verified).build());

        Project p7 = projectRepository.save(Project.builder()
                .user(owner2).kategori(catGambut).namaProject("Perkebunan Sawit Berkelanjutan")
                .lokasi("Sumatera, Indonesia")
                .koordinatLat(new BigDecimal("0.5000000")).koordinatLng(new BigDecimal("101.5000000"))
                .luasLahan(new BigDecimal("8000.00"))
                .deskripsi("Praktik penanaman sawit ramah lingkungan dengan perlindungan karbon.")
                .imageUrl("https://images.unsplash.com/photo-1590682680695-43b964a3ae17?w=800&q=80")
                .statusProject(ProjectStatus.verified).build());
        log.info("✓ 7 projects created");

        // --- MRV REPORTS ---
        var mrv1 = mrvReportRepository.save(MrvReport.builder()
                .project(p1).submittedByUser(owner).periodeMrv("2024-Q1")
                .koordinatGps("[{\"lat\":-1.2427,\"lng\":116.8528}]")
                .linkFotoSatelit("https://satellite.nusacarbon.co.id/borneo-q1-2024.jpg")
                .estimasiCo2e(new BigDecimal("10000.0000"))
                .catatan("Pengukuran pertama pasca penanaman mangrove")
                .statusMrv(MrvStatus.reviewed).build());

        var mrv2 = mrvReportRepository.save(MrvReport.builder()
                .project(p2).submittedByUser(owner2).periodeMrv("2024-Q1")
                .koordinatGps("[{\"lat\":-8.3405,\"lng\":115.092}]")
                .linkFotoSatelit("https://satellite.nusacarbon.co.id/bali-solar-q1.jpg")
                .estimasiCo2e(new BigDecimal("5000.0000"))
                .catatan("Output panel surya periode Q1 2024")
                .statusMrv(MrvStatus.reviewed).build());

        var mrv3 = mrvReportRepository.save(MrvReport.builder()
                .project(p3).submittedByUser(owner).periodeMrv("2024-Q1")
                .koordinatGps("[{\"lat\":0.5897,\"lng\":101.3431}]")
                .estimasiCo2e(new BigDecimal("12500.0000"))
                .catatan("Monitoring deforestasi Q1 — zero encroachment confirmed")
                .statusMrv(MrvStatus.reviewed).build());
        log.info("✓ 3 MRV reports created");

        // --- VERIFICATIONS ---
        var v1 = verificationRepository.save(Verification.builder()
                .mrvReport(mrv1).verifier(verifier).hasil(VerificationResult.approved)
                .volumeCo2eDisetujui(new BigDecimal("10000.0000"))
                .catatanAudit("Data satelit valid. Volume CO2e disetujui sesuai estimasi.").build());

        var v2 = verificationRepository.save(Verification.builder()
                .mrvReport(mrv2).verifier(verifier).hasil(VerificationResult.approved)
                .volumeCo2eDisetujui(new BigDecimal("5000.0000"))
                .catatanAudit("Output solar panel terverifikasi.").build());

        var v3 = verificationRepository.save(Verification.builder()
                .mrvReport(mrv3).verifier(verifier).hasil(VerificationResult.approved)
                .volumeCo2eDisetujui(new BigDecimal("12500.0000"))
                .catatanAudit("Zero deforestation confirmed by satellite analysis.").build());
        log.info("✓ 3 verifications created (all approved)");

        // --- CARBON TOKENS ---

        String buyerAddress = "0x742d355Cc6634C853925a3b944fc9ef13a";
        String genesisAddr = "0x0000000000000000000000000000000000000000";

        String prevHash = BlockchainHashUtil.GENESIS_HASH;
        int blockNum = 0;
        int totalTokensMinted = 0;

        
        // ─── Owner tokens (project owners keep some tokens for listings) ───────────────
        
        // P1: owner listed 5 tokens
        for (int i = 1; i <= 5; i++) {
            String serial = String.format("NC-2024-%03d-%06d", p1.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            CarbonToken token = tokenRepository.save(CarbonToken.builder()
                    .project(p1).verification(v1).owner(owner)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.listed)
                    .txMintHash(txHash).build());
            prevHash = txHash;
        }

        // P2: owner2 listed 5 tokens
        for (int i = 1; i <= 5; i++) {
            String serial = String.format("NC-2024-%03d-%06d", p2.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            CarbonToken token = tokenRepository.save(CarbonToken.builder()
                    .project(p2).verification(v2).owner(owner2)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.listed)
                    .txMintHash(txHash).build());
            prevHash = txHash;
        }

        // P3: owner listed 5 tokens
        for (int i = 1; i <= 5; i++) {
            String serial = String.format("NC-2024-%03d-%06d", p3.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            CarbonToken token = tokenRepository.save(CarbonToken.builder()
                    .project(p3).verification(v3).owner(owner)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.listed)
                    .txMintHash(txHash).build());
            prevHash = txHash;
        }

        // P6: owner listed 150 tokens
        for (int i = 1; i <= 150; i++) {
            String serial = String.format("NC-2024-%03d-%06d", p6.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            CarbonToken token = tokenRepository.save(CarbonToken.builder()
                    .project(p6).verification(v1).owner(owner)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.listed)
                    .txMintHash(txHash).build());
            prevHash = txHash;
        }

        // P7: owner2 listed 500 tokens
        for (int i = 1; i <= 500; i++) {
            String serial = String.format("NC-2024-%03d-%06d", p7.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            CarbonToken token = tokenRepository.save(CarbonToken.builder()
                    .project(p7).verification(v1).owner(owner2)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.listed)
                    .txMintHash(txHash).build());
            prevHash = txHash;
        }

        // ─── BUYER tokens (user 1 buys from ALL active projects) ──────────
        // Buyer owns tokens from every verified project to show interconnection

        // Buyer: 50 tokens from p1 (Mangrove Restoration Borneo) - sold
        for (int i = 1; i <= 50; i++) {
            String serial = String.format("NC-2024-%03d-B%05d", p1.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            tokenRepository.save(CarbonToken.builder()
                    .project(p1).verification(v1).owner(buyer)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.listed) // Let's make this one listed
                    .txMintHash(txHash).build());
            ledgerRepository.save(BlockchainLedger.builder()
                    .blockNumber(blockNum).txHash(txHash).prevHash(prevHash)
                    .txType(BlockchainTxType.mint)
                    .refId(blockNum).refTable("carbon_tokens")
                    .amountCo2e(BigDecimal.ONE)
                    .fromAddress(genesisAddr).toAddress(buyerAddress)
                    .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee())).build());
            prevHash = txHash;
            totalTokensMinted++;
        }

        // Buyer: 30 tokens from p2 (Solar Farm Bali) - sold
        for (int i = 1; i <= 30; i++) {
            String serial = String.format("NC-2024-%03d-B%05d", p2.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            tokenRepository.save(CarbonToken.builder()
                    .project(p2).verification(v2).owner(buyer)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.available)
                    .txMintHash(txHash).build());
            ledgerRepository.save(BlockchainLedger.builder()
                    .blockNumber(blockNum).txHash(txHash).prevHash(prevHash)
                    .txType(BlockchainTxType.mint)
                    .refId(blockNum).refTable("carbon_tokens")
                    .amountCo2e(BigDecimal.ONE)
                    .fromAddress(genesisAddr).toAddress(buyerAddress)
                    .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee())).build());
            prevHash = txHash;
            totalTokensMinted++;
        }

        // Buyer: 25 tokens from p3 (Rainforest Conservation) - sold
        for (int i = 1; i <= 25; i++) {
            String serial = String.format("NC-2024-%03d-B%05d", p3.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            tokenRepository.save(CarbonToken.builder()
                    .project(p3).verification(v3).owner(buyer)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.available)
                    .txMintHash(txHash).build());
            ledgerRepository.save(BlockchainLedger.builder()
                    .blockNumber(blockNum).txHash(txHash).prevHash(prevHash)
                    .txType(BlockchainTxType.mint)
                    .refId(blockNum).refTable("carbon_tokens")
                    .amountCo2e(BigDecimal.ONE)
                    .fromAddress(genesisAddr).toAddress(buyerAddress)
                    .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee())).build());
            prevHash = txHash;
            totalTokensMinted++;
        }

        // Buyer: 15 tokens from p4 (Wind Farm Java) - sold
        for (int i = 1; i <= 15; i++) {
            String serial = String.format("NC-2024-%03d-B%05d", p4.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            tokenRepository.save(CarbonToken.builder()
                    .project(p4).verification(v2).owner(buyer)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.retired) // Make these retired
                    .txMintHash(txHash).build());
            ledgerRepository.save(BlockchainLedger.builder()
                    .blockNumber(blockNum).txHash(txHash).prevHash(prevHash)
                    .txType(BlockchainTxType.mint)
                    .refId(blockNum).refTable("carbon_tokens")
                    .amountCo2e(BigDecimal.ONE)
                    .fromAddress(genesisAddr).toAddress(buyerAddress)
                    .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee())).build());
            prevHash = txHash;
            totalTokensMinted++;
        }

        // Buyer: 60 tokens from p6 (Hutan Pinus Sumatera) - sold
        for (int i = 1; i <= 60; i++) {
            String serial = String.format("NC-2024-%03d-B%05d", p6.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            tokenRepository.save(CarbonToken.builder()
                    .project(p6).verification(v1).owner(buyer)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.available)
                    .txMintHash(txHash).build());
            ledgerRepository.save(BlockchainLedger.builder()
                    .blockNumber(blockNum).txHash(txHash).prevHash(prevHash)
                    .txType(BlockchainTxType.mint)
                    .refId(blockNum).refTable("carbon_tokens")
                    .amountCo2e(BigDecimal.ONE)
                    .fromAddress(genesisAddr).toAddress(buyerAddress)
                    .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee())).build());
            prevHash = txHash;
            totalTokensMinted++;
        }

        // Buyer: 23 tokens from p7 (Perkebunan Sawit Berkelanjutan) - sold
        for (int i = 1; i <= 23; i++) {
            String serial = String.format("NC-2024-%03d-B%05d", p7.getIdProject(), i);
            blockNum++;
            String txHash = BlockchainHashUtil.generateTxHash(prevHash, "mint", 1.0, blockNum, LocalDateTime.now().toString());
            tokenRepository.save(CarbonToken.builder()
                    .project(p7).verification(v1).owner(buyer)
                    .tokenSerial(serial).vintageYear(2024)
                    .statusToken(TokenStatus.available)
                    .txMintHash(txHash).build());
            ledgerRepository.save(BlockchainLedger.builder()
                    .blockNumber(blockNum).txHash(txHash).prevHash(prevHash)
                    .txType(BlockchainTxType.mint)
                    .refId(blockNum).refTable("carbon_tokens")
                    .amountCo2e(BigDecimal.ONE)
                    .fromAddress(genesisAddr).toAddress(buyerAddress)
                    .gasFeeMock(BigDecimal.valueOf(BlockchainHashUtil.mockGasFee())).build());
            prevHash = txHash;
            totalTokensMinted++;
        }

        log.info("✓ {} carbon tokens minted + {} blockchain ledger entries created", totalTokensMinted, blockNum);

        // --- LISTINGS ---
        listingRepository.save(Listing.builder()
                .seller(owner).project(p1)
                .hargaPerToken(new BigDecimal("5000.00")).jumlahToken(5)
                .statusListing(ListingStatus.active).build());

        listingRepository.save(Listing.builder()
                .seller(owner2).project(p2)
                .hargaPerToken(new BigDecimal("5000.00")).jumlahToken(5)
                .statusListing(ListingStatus.active).build());

        listingRepository.save(Listing.builder()
                .seller(owner).project(p3)
                .hargaPerToken(new BigDecimal("5000.00")).jumlahToken(5)
                .statusListing(ListingStatus.active).build());

        listingRepository.save(Listing.builder()
                .seller(owner).project(p6)
                .hargaPerToken(new BigDecimal("5000.00")).jumlahToken(150)
                .statusListing(ListingStatus.active).build());

        listingRepository.save(Listing.builder()
                .seller(owner2).project(p7)
                .hargaPerToken(new BigDecimal("5000.00")).jumlahToken(500)
                .statusListing(ListingStatus.active).build());
        log.info("✓ 5 marketplace listings created");

        log.info("=== NusaCarbon database seeding completed ===");
    }
}
