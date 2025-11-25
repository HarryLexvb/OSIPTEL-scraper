# Quick Start Guide - GitHub Upload

## 🎯 Complete Command List

Copy and paste these commands in PowerShell (in order):

### 1. Navigate to Project Directory
```powershell
cd "C:\Users\harry\OneDrive\Documentos\visual studio\Proyectos Ventamon\osiptel scraper"
```

### 2. Configure Git (First Time Only)
```powershell
git config --global user.name "Harold Alejandro Villanueva Borda"
git config --global user.email "your.email@example.com"
```

### 3. Initialize Repository
```powershell
git init
```

### 4. Add All Files
```powershell
git add .
```

### 5. Create Initial Commit
```powershell
git commit -m "Initial commit: OSIPTEL Scraper v1.0.0 - Automated telephone line data extraction from OSIPTEL database with sequential processing - Author: Harold Alejandro Villanueva Borda"
```

### 6. Create GitHub Repository
- Go to https://github.com/new
- Repository name: `osiptel-scraper`
- Description: `Automated web scraper for extracting telephone line information from OSIPTEL (Peruvian Telecommunications Regulator) database. Sequential processing to avoid bans.`
- Visibility: Public
- **Don't** initialize with README, .gitignore, or license
- Click "Create repository"

### 7. Connect and Push
Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/osiptel-scraper.git
git branch -M main
git push -u origin main
```

---

## 📋 Repository Configuration

**Name:** `osiptel-scraper`

**Description:**
```
Automated web scraper for extracting telephone line information from OSIPTEL (Peruvian Telecommunications Regulator) database. Supports single RUC queries and batch processing from CSV/Excel files with sequential processing to avoid server bans.
```

**Topics:**
```
web-scraping, automation, osiptel, peru, telecommunications, python, camoufox, data-extraction, ruc-query, business-intelligence
```

---

## ✅ Done!

Your project is now on GitHub with:
- ✅ Complete documentation (README.md)
- ✅ MIT License protecting your authorship
- ✅ Proper .gitignore
- ✅ Professional code structure
- ✅ Copyright © 2025 Harold Alejandro Villanueva Borda

---

**Copyright © 2025 Harold Alejandro Villanueva Borda. All rights reserved.**
