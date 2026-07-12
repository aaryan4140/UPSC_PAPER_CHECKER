# UPSC Answer Evaluator — Setup Guide (Windows)

---

## Step 1: Install Python

1. Download from **https://www.python.org/downloads/**
2. Run installer → **CHECK "Add Python to PATH"** → Install Now

---

## Step 2: Install Poppler (for PDF preview)

1. Download from **https://github.com/oschwartz10612/poppler-windows/releases** (latest `.zip`)
2. Extract to `C:\poppler`
3. Add `C:\poppler\Library\bin` to system PATH:
   - Search "Environment Variables" → Edit system variables → Path → New → `C:\poppler\Library\bin` → OK

> Skip this if you don't need PDF page preview. Tool still works without it.

---

## Step 3: Create project folder

Open Command Prompt and run:
```
cd %USERPROFILE%\Desktop
mkdir Paper
cd Paper
```

---

## Step 4: Get the code

**Option A — With Git:**
```
git clone -b main https://github.com/aaryan4140/UPSC_PAPER_CHECKER.git .
```

**Option B — Without Git:**
1. Download ZIP from GitHub (green "Code" button → Download ZIP)
2. Extract the contents **into** the `Paper` folder on your Desktop

---

## Step 5: Add API Key

1. Copy `.env.example` → Rename copy to `.env`
2. Open `.env` with Notepad → Replace `paste_your_api_key_here` with your key → Save

---

## Step 6: First Launch

Double-click **`start.bat`** inside the Paper folder. First run installs everything (2-3 min).

---

## Step 7: Create Desktop Shortcut

Double-click **`create_shortcut.bat`** inside the Paper folder. UPSC Evaluator icon appears on Desktop.

---

## Daily Use

Double-click the **UPSC Evaluator** icon on Desktop.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Python not found" | Reinstall Python, check "Add to PATH" |
| "Failed to install" | Check internet, run `start.bat` again |
| "API key not configured" | Check `.env` file |
| "Evaluation failed" | API quota exhausted, wait or swap key |
| "Preview unavailable" | Poppler not installed (Step 2) |
| Browser won't open | Go to **http://localhost:8501** manually |
| Can't see `.env` file | File Explorer → View → Show file extensions |

---

## Stop the App

Press `Ctrl+C` in the terminal window, or close it.

---

## Update to New Version

```
cd %USERPROFILE%\Desktop\Paper
git pull
```
Then double-click `start.bat` again. If no Git, re-download ZIP, replace folder (keep `.env`), delete `venv`, run `start.bat`.
