# 🌿 NusaCarbon - Tokenized Carbon Credit Platform

[![PHP Version](https://img.shields.io/badge/PHP-8.2%2B-777BB4?style=flat-square&logo=php)](https://php.net)
[![MySQL Version](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql)](https://mysql.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![Railway](https://img.shields.io/badge/Deployment-Railway-0B0D0E?style=flat-square&logo=railway)](https://railway.app)

NusaCarbon is a complete end-to-end marketplace mock-up for tokenized carbon credits (tCO₂e) aimed at mitigating climate change. Built specifically for the Indonesian market, it bridges the gap between environmental project owners and corporate buyers through a transparent, immutable, blockchain-inspired mock ledger. 

The application implements a robust **Role-Based Access Control (RBAC)** architecture and digital **Monitoring, Reporting & Verification (dMRV)** workflows without replying on third-party frameworks.

## 🏗 System Architecture & Features

The platform operates using four distinct user archetypes. Each acts within a closed ecosystem that maintains strict segregation of capabilities:

1. **Buyer (Corporate & Personal)**
   - Access to the public Carbon Marketplace.
   - Generation of unique cryptographic wallet addresses.
   - Capability to purchase carbon tokens and permanently **Retire** (burn) them from circulation.
   - Automatic generation of verified Carbon Offset Certificates upon retirement.

2. **Project Owner**
   - Submit new environmental projects (e.g., Forestry, Mangroves, Renewable Energy).
   - Track project validation status and view minted total token issuances.

3. **Verifier (Independent Auditor)**
   - Conduct strict due diligence on pending environmental projects.
   - Execute the **Token Minting** process upon successful project verification.

4. **Administrator**
   - Platform oversight and **Customer Due Diligence (KYC)**.
   - Approve or Reject new user registrations to ensure corporate compliance.

### ⛓ The Blockchain Ledger Simulation
NusaCarbon utilizes a specialized SQL table (`blockchain_ledger`) intentionally designed to mimic blockchain dynamics. 
- **Append-Only:** No `UPDATE` or `DELETE` queries are ever executed against the ledger.
- **Cryptographic Hashing:** Every transaction calculates a SHA-256 hash derived from the `(previous_hash + sender + receiver + amount + timestamp)`, ensuring immutability and complete provenance tracking.

---

## 🛠 Technology Stack

This project was intentionally engineered using a fundamental (Vanilla) architecture to demonstrate core web execution without framework abstraction overhead:

- **Backend Logic:** PHP 8.2 (Procedural & PDO Object-Oriented Hybrid)
- **Database:** MySQL 8.0 (Strict Relational PDM)
- **Frontend UI/UX:** HTML5, Premium CSS3 Variables (Glassmorphism & Gradients), Vanilla JavaScript.
- **Iconography:** Lucide Icons (CDN)
- **Containerization & CI/CD:** Docker Compose (Local) and Nixpacks (Railway Cloud Deployment).

---

## 🚀 Getting Started (Local Development)

The preferred method for local execution is through Docker, which orchestrates both the PHP/Apache server and the MySQL database environment seamlessly.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine.

### Installation
1. Clone this repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Skyiop1/CS-Fundamentals-UNAIR.git
   cd CS-Fundamentals-UNAIR/NusaCarbonWEB/nusacarbon-web
   ```
2. Build and spin up the Docker containers:
   ```bash
   docker compose up -d
   ```
3. The server will initialize and automatically run the `schema.sql` and `seed.sql` inside the database.
4. Access the platform via your browser at: **http://localhost:8000**

---

## ☁️ Production Deployment (Railway)

NusaCarbon is highly optimized for deployment on [Railway.app](https://railway.app/).

1. Connect your GitHub repository to Railway.
2. Provision a **MySQL Database** service on Railway.
3. In your Web Service settings, define the following **Root Directory**:
   `/NusaCarbonWEB/nusacarbon-web`
4. In your Web Service **Variables/Environment** tab, simply reference:
   `MYSQL_PUBLIC_URL` pointing strictly to your Railway MySQL Database service URL.
5. Railway's Nixpacks will detect `composer.json`, automatically build the PHP 8.2 environment, inject `pdo_mysql` extensions, and safely expose the web application.

---

## 🔐 Built-In Test Users

For immediate testing, evaluate the system using the pre-seeded mockup accounts. The password for all accounts below is exclusively **`password123`**:

| User Persona | Email Address | Assigned Role |
| :--- | :--- | :--- |
| **Buyer** | `buyer@nusacarbon.id` | Buyer |
| **Project Owner**| `owner@nusacarbon.id` | Project Owner |
| **Verifier** | `verifier@nusacarbon.id` | Verifier/Auditor |
| **Administrator**| `admin@nusacarbon.id` | Global Admin |

---
*Developed for Academic & CS Fundamental Demonstrations @ UNAIR.*
