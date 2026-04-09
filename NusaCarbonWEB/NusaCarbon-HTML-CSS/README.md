# 🎨 NusaCarbon - Static UI/UX Prototype

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

> **⚠️ IMPORTANT NOTICE:** This directory contains **ONLY** the static HTML, CSS wireframes, and initial prototypes. 
> For the completely functional backend application (PHP, MySQL, Authentication, Blockchain simulation), please navigate to the `../nusacarbon-web/` directory.

## 📖 Overview

The `NusaCarbon-HTML-CSS` module serves as the foundational design system and visual blueprint for the entire NusaCarbon platform. By building everything from scratch (without UI frameworks like Tailwind or Bootstrap), this prototype establishes a highly customized, premium web ecosystem.

The aesthetic direction focuses heavily on **Glassmorphism**, vibrant climate-inspired gradients (Emerald & Teal), and sleek, enterprise-grade data visualization.

---

## 🎨 Design System Anatomy

Instead of relying on heavy pre-processor files, the entire stylistic ecosystem is powered natively by highly systematic CSS Variables (`/assets/css/style.css`).

### Core Color Tokens
- `--color-primary`: `#059669` (Digital Emerald)
- `--color-secondary`: `#0ea5e9` (Sky Blue Offset)
- `--gradient-hero`: A deep-space teal gradient representing blockchain modernism mixed with environmental hues.

### Key Visual Paradigms
- **Glassmorphism**: Soft background blurs (`backdrop-filter: blur()`) paired with ultra-thin translucent borders.
- **Micro-interactions**: Scale transformations, glowing hover states, and smooth bezier-curve transitions across interactive components.
- **Card-Based UI**: Segmenting logic visually for different roles (Admin, Buyer, Verifier, Project Owner).

---

## 📂 File Map (Wireframes)

This folder includes hardcoded templates that were later abstracted into PHP includes. You can open any of these natively in a browser to view the pure HTML output.

- `index.html`: The introductory Role Selector landing page.
- `login.html` & `register.html`: Authentication mocked forms.
- `marketplace.html`: The grid interface for viewing listed tokenized projects.
- `buyer-dashboard.html`: The corporate wallet tracking UI.
- `owner-dashboard.html`: Project metrics and token minting status UI.
- `form-project.html`: Complex data ingestion forms for registering eco-projects.

---

## 💡 How to Use
Since this directory is purely static:
1. You do not need a local server (like Apache or Node.js) to run this.
2. Simply double-click any `.html` file (e.g., `index.html`) to open it directly in Google Chrome, Safari, or Firefox.

If you are looking to see the actual database logic, token retirements, or the simulated blockchain ledger in action, please run the Docker environment found in the **`../nusacarbon-web/`** directory.
