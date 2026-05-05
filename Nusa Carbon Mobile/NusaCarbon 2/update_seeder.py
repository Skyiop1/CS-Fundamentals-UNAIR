import re

with open("src/main/java/com/nusacarbon/api/config/DataSeeder.java", "r") as f:
    code = f.read()

# Replace the manual single token minting with loops that mint enough tokens for the listings
replacement = """
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
"""

# Find the block from line 210 up to 273 and replace it
start_idx = code.find("// ─── Owner tokens (project owners keep some tokens)")
end_idx = code.find("// ─── BUYER tokens (user 1 buys from ALL active projects) ──────────")

if start_idx != -1 and end_idx != -1:
    new_code = code[:start_idx] + replacement + "\n        " + code[end_idx:]
    with open("src/main/java/com/nusacarbon/api/config/DataSeeder.java", "w") as f:
        f.write(new_code)
    print("Replaced owner token seeding block.")
else:
    print("Could not find start or end index")

