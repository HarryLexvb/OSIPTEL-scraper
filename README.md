# OSIPTEL Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Author:** Harold Alejandro Villanueva Borda  
**Version:** 1.0.0  
**License:** MIT

## 📋 Description

OSIPTEL Scraper is an automated tool designed to extract telephone line information from the OSIPTEL (Organismo Supervisor de Inversión Privada en Telecomunicaciones - Peruvian Telecommunications Regulator) database. This tool enables efficient data collection for business analysis, compliance verification, and telecommunications research.

### Key Features

- ✅ **Single RUC Query**: Search for telephone lines associated with a specific RUC (Tax ID)
- ✅ **Batch Processing**: Process multiple RUCs from CSV or Excel files
- ✅ **Sequential Processing**: One-by-one processing to avoid server bans
- ✅ **Automated Data Export**: Results exported to CSV with indexed columns
- ✅ **Error Handling**: Robust error management and detailed logging
- ✅ **Stealth Mode**: Humanized browsing behavior to avoid detection

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Windows, macOS, or Linux

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/osiptel-scraper.git
cd osiptel-scraper
```

### Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## 📖 Usage

### Running the Script

```bash
python scraperOsiptel.py
```

### Option 1: Single RUC Query

1. Select option `1` from the menu
2. Enter the RUC number (11 digits)
3. Wait for the scraping process to complete
4. Results will be saved as `resultado_[RUC]_[timestamp].csv`

**Example:**
```
Ingrese opción (1 o 2): 1
Ingrese el RUC: 20515589873
```

### Option 2: Batch Processing from File

1. Prepare a CSV or Excel file with RUCs in the first column
2. Select option `2` from the menu
3. Enter the file path
4. Wait for all RUCs to be processed
5. Results will be saved as `resultados_osiptel_[timestamp].csv`

**Example CSV format:**
```csv
RUC
20515589873
20104605223
20490920081
```

**Example Excel format:**
```
| RUC         |
|-------------|
| 20515589873 |
| 20104605223 |
| 20490920081 |
```

## 📊 Output Format

The script generates a CSV file with the following structure:

| RUC         | Modalidad_1 | Número_Telefónico_1 | Empresa_Operadora_1 | Modalidad_2 | ... |
|-------------|-------------|---------------------|---------------------|-------------|-----|
| 20515589873 | CONTROL     | 99401****           | ENTEL PERU S.A.     | CONTROL     | ... |
| 20104605223 | POSTPAGO    | 98251****           | AMERICA MOVIL PERU  |             |     |

### Column Explanation

- **RUC**: Tax identification number
- **Modalidad_N**: Service type (CONTROL, POSTPAGO, PREPAGO)
- **Número_Telefónico_N**: Phone number (partially masked for privacy)
- **Empresa_Operadora_N**: Telecommunications operator company

*Note: Each RUC can have multiple lines, indexed with _1, _2, _3, etc.*

## ⚙️ Configuration

### Processing Speed

The script processes RUCs **sequentially** (one by one) with a 2-second delay between requests. This approach:

- ✅ Prevents server bans and IP blocking
- ✅ Ensures data accuracy
- ✅ Maintains stable connection
- ⚠️ Takes longer for large datasets (~30 seconds per RUC)

### Timeout Settings

- **Browser timeout**: 120 seconds
- **Page load**: Waits for network idle state
- **Table rendering**: 6 seconds initial wait + 5 seconds after selector change

## 🛡️ Legal & Ethical Considerations

### Important Notice

This tool is designed for **legitimate business purposes only**:

- ✅ Compliance verification
- ✅ Business intelligence
- ✅ Telecommunications research
- ✅ Data validation

### Usage Guidelines

- **Rate Limiting**: The script implements delays to respect server resources
- **Data Privacy**: Handle extracted data responsibly and in compliance with privacy laws
- **Terms of Service**: Users are responsible for complying with OSIPTEL's terms of use
- **No Warranty**: This software is provided "as is" without warranty of any kind

### Disclaimer

The author (Harold Alejandro Villanueva Borda) and contributors are not responsible for misuse of this tool. Users assume full responsibility for their actions and must comply with all applicable laws and regulations.

## 🔧 Troubleshooting

### Common Issues

**1. Browser doesn't open / Script hangs**
- Ensure you have stable internet connection
- Check firewall settings
- Verify Camoufox installation: `pip install --upgrade camoufox`

**2. "No telephone lines" for valid RUCs**
- Some RUCs may legitimately have no registered lines
- Check if RUC format is correct (11 digits)
- Verify RUC exists in OSIPTEL database

**3. Import errors**
```bash
pip install --upgrade -r requirements.txt
```

**4. Permission denied errors (Windows)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📦 Dependencies

- **camoufox** (0.4.11): Stealth browser automation
- **pandas** (2.2.0): Data manipulation and CSV/Excel handling
- **openpyxl** (3.1.2): Excel file support

See `requirements.txt` for complete list with versions.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/osiptel-scraper.git
cd osiptel-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows

# Install in development mode
pip install -r requirements.txt
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ No warranty
- ⚠️ No liability

## 👤 Author

**Harold Alejandro Villanueva Borda**

- GitHub: [@YOUR_GITHUB_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- OSIPTEL for providing the public database
- Camoufox team for the stealth browser framework
- Python community for excellent libraries and tools

## 📈 Roadmap

Future improvements planned:

- [ ] Add GUI interface
- [ ] Support for DNI (National ID) queries
- [ ] Export to Excel with formatting
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Web API wrapper
- [ ] Docker containerization

## 📞 Support

For questions, issues, or suggestions:

1. Check [Troubleshooting](#-troubleshooting) section
2. Review [Issues](https://github.com/YOUR_USERNAME/osiptel-scraper/issues) on GitHub
3. Open a new issue if needed

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**

**Copyright © 2025 Harold Alejandro Villanueva Borda. All rights reserved.**
