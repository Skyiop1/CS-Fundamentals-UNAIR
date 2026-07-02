# NusaCarbon Mobile App

📱 **Flutter Mobile Application** for NusaCarbon — Indonesia's blockchain-inspired carbon credit token marketplace.

> **Tagline:** "Transparent. Verified. Tokenized Carbon Credits."

---

## 📋 Overview

NusaCarbon Mobile is the client-side mobile application of the NusaCarbon ecosystem. It is designed to provide project owners and buyers with a seamless interface for managing tokenized carbon credits, submitting digital Monitoring, Reporting & Verification (dMRV) documents, and visualizing impact metrics.

---

## 💎 Features

- **Dashboard & Portfolio Tracking**: Emerald-to-teal visual indicators showing active carbon portfolio value, token distributions, and historical transaction graphs.
- **dMRV Submissions**: Dedicated project upload interface for environmental verification documents.
- **Blockchain Simulator**: Interactive local simulation showing mock transaction hash updates, blocks confirmation, and blockchain ledger state.
- **Wallet & Token Manager**: Purchase, trade, and retire carbon tokens directly from the app interface.
- **Dockerized Backend Integration**: Works seamlessly with the Spring Boot API service running in containerized environments.

---

## 🛠️ Tech Stack

- **Framework**: [Flutter](https://flutter.dev/) (Dart)
- **Local Databases**: SQLite / shared_preferences
- **State Management**: Provider / BLoC
- **API Client**: HTTP package with local service integration
- **Styling**: Emerald brand design guidelines

---

## 🚀 Getting Started

### Prerequisites

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (3.x recommended)
- Android Studio / VS Code with Dart & Flutter extensions
- Android Emulator / physical device for testing

### Installation

1. Navigate to the project directory:
   ```bash
   cd "Nusa Carbon Mobile/nusacarbon_app/nusacarbon"
   ```
2. Fetch Dart dependencies:
   ```bash
   flutter pub get
   ```
3. Run the application:
   ```bash
   flutter run
   ```

---

## 📂 Directory Structure

```
Nusa Carbon Mobile/
├── README.md                              # This file
├── nusacarbon_app/
│   ├── Nusacarbon brand guidelines.md     # Styling & UI guidelines
│   ├── Nusacarbon system instructions.md  # System setup files
│   └── nusacarbon/                        # Flutter project root
│       ├── lib/                           # Source files
│       ├── android/                       # Android configuration
│       ├── ios/                           # iOS configuration
│       └── web/                           # Web deployment files
```
