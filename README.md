# Web Scraper Pro - README.md

A powerful and user-friendly GUI application for scraping web pages, built with Python, Tkinter, and BeautifulSoup. It supports both single-page scraping and batch scraping with multiple output formats.

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Single Page Scraping](#-single-page-scraping)
  - [Batch Scraping](#-batch-scraping)
  - [Settings](#️-settings)
  - [History](#-history)
- [Output Formats](#-output-formats)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

- **Single Page Scraping** — Scrape any URL instantly and preview the result
- **Batch Scraping** — Scrape hundreds of URLs from a text file with configurable delays
- **Multiple Output Formats** — Markdown (`.md`), Plain Text (`.txt`), and JSON (`.json`)
- **Smart Filenames** — Auto-generated unique filenames using page title + URL suffix
- **Customizable User Agents** — Random or custom User-Agent headers to avoid blocking
- **Configurable Timeouts** — Adjust request timeouts to suit your network
- **History Viewer** — Browse, open, or delete previously scraped files
- **Save/Load Settings** — Persist preferences between sessions
- **Live Progress & Logging** — Real-time progress bar and detailed scraping log

---

## 🧰 Requirements

- **Python** 3.7 or higher
- **pip** (Python package manager)

### Python Dependencies

- `requests`
- `beautifulsoup4`
- `tkinter` (usually bundled with Python)

---

## 🚀 Installation

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/web-scraper-pro.git
cd web-scraper-pro
```

Or simply download `scraper_gui.py` and place it in a folder of your choice.

### 2. (Optional) Create a virtual environment

**On Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**

```bash
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install requests beautifulsoup4
```

### 4. Install Tkinter (if not already installed)

**Ubuntu / Debian:**

```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora / RHEL:**

```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**

```bash
sudo pacman -S tk
```

**macOS (via Homebrew):**

```bash
brew install python-tk
```

**Windows:** Tkinter is bundled with the official Python installer — no extra steps needed.

---

## 🖥️ Usage

### Launch the application

```bash
python scraper_gui.py
```

On Linux/macOS, if `python` is not found, use:

```bash
python3 scraper_gui.py
```

The GUI will open with four tabs: **Single Page**, **Batch Scraper**, **Settings**, and **History**.

---

### 🔗 Single Page Scraping

1. Open the **Single Page** tab.
2. Enter the URL (e.g., `https://example.com/article`).
3. Choose an output format:
   - **Markdown (.md)** — Compact, human-readable
   - **Text (.txt)** — Simple plain text
   - **JSON (.json)** — Machine-readable
4. Click **🚀 Scrape Page**.
5. The result is saved to the output folder and previewed in the app.

**Example:**

```
URL: https://en.wikipedia.org/wiki/Web_scraping
Format: Markdown (.md)
→ Saved as: Web_scraping_-_Wikipedia_iki1.md
```

Use **🗑️ Clear** to reset the output area.

---

### 📚 Batch Scraping

1. Open the **Batch Scraper** tab.
2. Click **Browse** to select a `.txt` file containing URLs (one per line).
3. Or click **Create Sample** to generate a starter file.
4. Configure:
   - **Delay (seconds)** — Wait time between requests (default: `20`)
   - **Output Folder** — Where files will be saved (default: `scraped_pages`)
5. Click **▶️ Start Batch Scraping**.
6. Monitor progress via the progress bar and log.
7. Click **⏹️ Stop** to cancel mid-run.

**Example URLs file (`urls.txt`):**

```
# Sample URLs File
# Add your URLs below (one per line)
# Lines starting with # are ignored

https://example.com/article1
https://example.com/article2
https://example.com/article3
```

**Run batch scraping from the GUI** — no command line needed. But if you want to prepare the file from the terminal:

```bash
cat > urls.txt <<EOF
# My scraping list
https://example.com/article1
https://example.com/article2
https://example.com/article3
EOF
```

---

### ⚙️ Settings

Open the **Settings** tab to configure:

| Setting | Description |
|---|---|
| Default Output Folder | Where scraped files are saved |
| User Agent | **Random** (recommended) or **Custom** |
| Custom User Agent | Only used when "Custom" is selected |
| Request Timeout | Seconds before giving up on a request (10–120) |

Click **💾 Save Settings** to persist to `scraper_settings.json`.

---

### 📜 History

- Lists all files in the output folder with size and modification date
- **🔄 Refresh** — Reload the list
- **📂 Open File** — Open the selected file with the system default app
- **🗑️ Delete** — Permanently remove the selected file

> **Note:** The **Open File** button uses `os.startfile()` which is Windows-only.  
> For macOS/Linux, edit the `open_selected_file` method:

```python
# macOS
os.system(f'open "{filepath}"')

# Linux
os.system(f'xdg-open "{filepath}"')
```

---

## 📄 Output Formats

### Markdown (`.md`)

```markdown
# Page Title

**Source:** https://example.com
**Extracted:** 2025-01-15 14:32:10

---

First paragraph of content...

Second paragraph of content...
```

### Text (`.txt`)

```
Title: Page Title
Source: https://example.com
Date: 2025-01-15 14:32:10
==================================================

First paragraph of content...
```

### JSON (`.json`)

```json
{
  "title": "Page Title",
  "url": "https://example.com",
  "date": "2025-01-15 14:32:10",
  "content": "First paragraph...\n\nSecond paragraph...",
  "paragraphs": 2
}
```

---

## 📁 Project Structure

```
web-scraper-pro/
├── scraper_gui.py            # Main GUI application
├── scraper_settings.json     # Auto-generated settings file
├── scraped_pages/            # Default output folder
│   ├── Page_Title_ab12.md
│   ├── Another_Article_cd34.md
│   └── ...
└── urls.txt                  # Optional: your batch URL list
```

---

## 🛠️ Troubleshooting

### `ModuleNotFoundError: No module named 'tkinter'`

Install Tkinter for your OS (see [Installation](#-installation)).

### `ModuleNotFoundError: No module named 'requests'` or `'bs4'`

```bash
pip install requests beautifulsoup4
```

### HTTP 403 / 429 errors

- Increase the **Delay** in Batch Settings (e.g., 30–60 seconds)
- Switch **User Agent** to **Custom** and paste a real browser UA string
- Some sites block scrapers — try a different site or use a proxy

### `requests.exceptions.Timeout`

Increase the **Request Timeout** in Settings.

### Unicode / encoding errors on Windows

Run the script in a UTF-8 capable terminal:

```bash
chcp 65001
python scraper_gui.py
```

### Permission denied when saving

Make sure the output folder is writable:

```bash
chmod -R u+w scraped_pages/
```

---

## 📜 License

This project is provided as-is for educational and personal use.  
Please respect the `robots.txt` and Terms of Service of any website you scrape.

---

## 🙌 Acknowledgements

- [Requests](https://requests.readthedocs.io/) — HTTP library
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework

---

**Happy scraping! 🕸️**
