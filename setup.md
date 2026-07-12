# UPSC Answer Evaluator — Setup Guide (Windows)

This guide will help you set up and run the UPSC Answer Evaluator on your Windows computer.

---

## Prerequisites

You will need:
- A Windows 10/11 computer
- Internet connection
- A Gemini API key (provided to you separately)

---

## Step 1: Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python 3.x.x"** button
3. Run the downloaded installer
4. **IMPORTANT:** On the first screen, check the box that says **"Add Python to PATH"**
5. Click **"Install Now"**
6. Wait for installation to finish, then close the installer

**To verify:** Open Command Prompt (search "cmd" in Start menu) and type:
```
python --version
```
You should see something like `Python 3.12.x` or `Python 3.13.x`.

---

## Step 2: Download the Project

**Option A — If you have Git installed:**
```
git clone https://github.com/YOUR_USERNAME/Paper.git
cd Paper
```

**Option B — Without Git:**
1. Go to the GitHub repository page
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP folder to a location you'll remember (e.g., Desktop or Documents)
5. Open the extracted folder

---

## Step 3: Run Setup

1. Open the project folder
2. Double-click **`setup.bat`**
3. Wait for it to finish (takes 2-3 minutes to install dependencies)
4. You'll see "Setup Complete!" when done

---

## Step 4: Add Your API Key

1. Open the file called **`.env`** in the project folder (use Notepad)
   - If you don't see `.env`, the setup created it from `.env.example`
   - If neither exists, copy `.env.example` and rename it to `.env`
2. Find the line: `GEMINI_API_KEY=paste_your_api_key_here`
3. Replace `paste_your_api_key_here` with the API key provided to you
4. Save and close the file

---

## Step 5: Install Poppler (for PDF Preview)

This is needed to show a visual preview of your uploaded PDF. The tool works without it, but you won't see the preview thumbnail.

1. Download Poppler from: [github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Download the latest `.zip` file (e.g., `Release-xx.xx.x-0.zip`)
3. Extract it to `C:\poppler\` (or any folder)
4. Add Poppler to PATH:
   - Search "Environment Variables" in Start menu
   - Click **"Edit the system environment variables"**
   - Click **"Environment Variables"** button
   - Under "System variables", find **Path**, click **Edit**
   - Click **New**, add: `C:\poppler\Library\bin`
   - Click OK on all windows
5. Restart your computer

**If this feels complicated, skip it.** The tool will still evaluate your papers — you just won't see the page preview.

---

## Step 6: Launch the App

1. Double-click **`start.bat`** in the project folder
2. A terminal window will open (keep it running)
3. Your browser will automatically open with the app
4. If the browser doesn't open, manually go to: `http://localhost:8501`

---

## How to Use

1. Click **"Answer Evaluation"** from the navigation
2. Select your **Subject** (Polity, Economics, Geography, etc.)
3. Adjust **Strictness** slider (default is 7/10)
4. Upload your handwritten answer sheet as a PDF
5. Click **"Evaluate Answer Sheet"**
6. Wait ~45-60 seconds for AI analysis
7. View your results: scores, rubric breakdown, model answers, and feedback

---

## Stopping the App

- Press `Ctrl + C` in the terminal window, OR
- Simply close the terminal window

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Reinstall Python and make sure to check "Add to PATH" |
| "Module not found" | Run `setup.bat` again |
| "API key not configured" | Check your `.env` file has the correct key |
| "Evaluation failed" | Your API quota may be exhausted — wait or use a different key |
| "Preview unavailable" | Poppler is not installed (Step 5) — the tool still works without it |
| Browser doesn't open | Manually go to `http://localhost:8501` |

---

## File Structure (for reference)

```
Paper/
├── setup.bat          ← Run once to install everything
├── start.bat          ← Double-click to launch the app
├── .env               ← Your API key goes here
├── .env.example       ← Template (don't edit this)
├── requirements.txt   ← Python packages list
├── app/               ← Application code
├── venv/              ← Created by setup (don't delete)
└── data/              ← Stores your evaluation history
```

---

## Need Help?

Contact the project owner for:
- API key issues
- Technical support
- Feature requests
