# ♿ AccessEase - Accessibility Assistant

AccessEase is an inclusive accessibility application built in Python for first-year college students. It empowers individuals with physical, sensory, and mobility requirements to evaluate public venues (Hospitals, Colleges, Malls, Railway/Metro Stations, and Public Buildings) before traveling.

---

## 🖥️ Two Ways to Run AccessEase

You now have both an **authentic native desktop application** and the optional browser web version:

| Application Type | Main File | How to Launch | Requirements |
| :--- | :--- | :--- | :--- |
| **Native Desktop App** *(Recommended)* | [`AccessEase.pyw`](file:///c:/Samprikta/Python-Mini-Project/AccessEase.pyw) or [`desktop_app.py`](file:///c:/Samprikta/Python-Mini-Project/desktop_app.py) | Double-click [`AccessEase.pyw`](file:///c:/Samprikta/Python-Mini-Project/AccessEase.pyw), double-click [`AccessEase.bat`](file:///c:/Samprikta/Python-Mini-Project/AccessEase.bat), or run `python desktop_app.py` | Python standard library (`tkinter` + `pandas`). **Zero browser needed!** |
| **Web Browser Version** | [`app.py`](file:///c:/Samprikta/Python-Mini-Project/app.py) | Double-click [`Launch_Website.bat`](file:///c:/Samprikta/Python-Mini-Project/Launch_Website.bat) or run `streamlit run app.py` | `streamlit`, `pandas` |

---

## 📁 Project Structure

```text
Python-Mini-Project/
│
├── AccessEase.pyw              # One-click native desktop app (runs with NO black terminal window)
├── AccessEase.bat              # One-click desktop app batch launcher
├── desktop_app.py              # Native Windows Desktop GUI Application (Tkinter & Canvas architecture)
├── theme.py                    # Design system tokens, color palettes, typography & rounded shape renderer
├── ui_components.py            # Reusable UI dialogs: Audit Details Modal, Filter Modal, Rounded Cards
│
├── logic.py                    # Shared backend calculation engine (Haversine formula, match score, filters)
├── data_manager.py             # CSV data persistence and loader utilities
├── test_logic.py               # Automated unit tests (13 test cases) verifying all algorithms
│
├── landmarks.csv               # 20 Reference starting anchor points in Pune (chowks, bridges, flyovers)
├── locations.csv               # 50 Destination venues with coordinates & 8 accessibility amenities
├── places.csv                  # Venue dataset synchronized with locations.csv
│
├── app.py                      # Interactive Streamlit Web Application (browser alternative)
├── Launch_Website.bat          # One-click web application batch launcher
│
├── AccessEase_User_Stories.docx# Professional Word Document with Agile User Stories & Epics
├── AccessEase_User_Stories.rtf # Universal Rich Text Document (compatible with all Word versions)
├── USER_STORIES.md             # Complete User Stories specification in Markdown
├── requirements.txt            # Python dependencies (pandas, streamlit, Pillow)
├── README.md                   # Complete project documentation & team presentation guide
│
└── assets/                     # Graphic assets, branding logos, hero banners, and venue photography
    ├── sidebar_logo_v2.png     # Centered AccessEase sidebar logo
    ├── sidebar_quote.png       # Centered bottom quote artwork ("Accessible today... Inclusive tomorrow ♡")
    ├── hero_art_v2.png         # Skyline & wheelchair emblem hero artwork
    ├── places/                 # Destination photography for venue cards
    └── icons/                  # Category icons
```

---

## 📄 User Stories Document
The complete Agile User Stories document is available in:
- **Microsoft Word format:** [`AccessEase_User_Stories.docx`](file:///c:/Samprikta/Python-Mini-Project/AccessEase_User_Stories.docx)
- **Markdown format:** [`USER_STORIES.md`](file:///c:/Samprikta/Python-Mini-Project/USER_STORIES.md)

It contains **16 detailed user stories across 7 epics**, covering personas, acceptance criteria (Given-When-Then), story points, priorities (MoSCoW), and a sprint traceability matrix.

---

## 🚀 How to Launch the Desktop Application

### Method 1: The One-Click Launcher (Easiest!)
Simply double-click the file **`AccessEase.bat`** in your project folder. A native desktop window will pop up immediately on your computer screen!

### Method 2: From VS Code Terminal
Open your VS Code terminal and run:
```powershell
python desktop_app.py
```
*(or `py desktop_app.py`)*

---

## 🌟 Key Features

1. **Modern Blue, Purple & White Theme**: Professional, high-contrast user interface adhering to accessibility design principles.
2. **Tri-State Accessibility Tracking**:
   - 🟢 **Available**: Facility physically verified as accessible.
   - 🔴 **Unavailable**: Facility confirmed absent.
   - ⚪ **Unknown / Unverified**: Missing/unreported data is **never** assumed to be unavailable.
3. **8 Essential Accessibility Criteria**:
   - Wheelchair Ramps
   - Step-free Entrances
   - Lifts
   - Accessible Toilets
   - Accessible Parking
   - Tactile Pathways
   - Audio Assistance
   - Large-text Signage
4. **Quick Accessibility Profiles**:
   - ♿ Wheelchair User Preset
   - 👁️ Visually Impaired Preset
   - 🚶 Mobility Difficulties Preset
   - ⚙️ Custom / Manual Selection
5. **Real-Time Match Scoring**: Calculates the percentage of chosen facilities available at each venue, sorting the best matches to the top.
6. **Detailed Facility Breakdown**: Expandable cards displaying contact details, audit notes, and a comprehensive status matrix.
7. **Saved Places (Bookmarks)**: Save important places for instant access across tabs during your session.
8. **Ethical Disclaimer Banner**: Clear notice highlighting that sample data is fictional and requires verification before real-world visits.

---

## 🚀 Quick Start Guide

### Step 1: Open Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File -> Open Folder...** and select `c:\Samprikta\Python-Mini-Project`.
3. Open the built-in terminal by pressing ``Ctrl + ` `` (Backtick) or going to **Terminal -> New Terminal**.

### Step 2: Set Up Virtual Environment (Recommended)
In your VS Code terminal, run:
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows (PowerShell):
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell shows an execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry)*
- On Windows (Command Prompt):
  ```cmd
  venv\Scripts\activate.bat
  ```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Run Unit Tests
Verify all core calculation and filtering logic works:
```bash
python test_logic.py
```
You should see:
```text
Ran 13 tests in 0.05s
OK
```

### Step 5: Launch the AccessEase Web App
```bash
streamlit run app.py
```
Streamlit will automatically open your default browser to:
`http://localhost:8501`

---

## 👥 4-Student Team Role Breakdown & Collaboration

| Student | Assigned Role | Primary Files & Deliverables | Core Viva Topics to Explain |
| :--- | :--- | :--- | :--- |
| **Student 1** | **Geospatial & Data Engineer** | `landmarks.csv`, `locations.csv`, `places.csv`, `data_manager.py` | • 2-tier spatial data model: 20 Reference starting landmarks vs. 50 Destination venues.<br>• Separation of concerns: why landmarks and destination venues never overlap.<br>• Ethical tri-state accessibility tracking (`Available`, `Unavailable`, `Unknown`). |
| **Student 2** | **Backend Algorithm & Logic Lead** | `logic.py`, `test_logic.py` | • Offline great-circle **Haversine Distance formula** using pure Python math ($R=6371\text{ km}$).<br>• Accessibility Match Score percentage algorithm with weighted profiles.<br>• Automated unit test suite with 13 comprehensive test cases. |
| **Student 3** | **Desktop GUI & Frontend Architect** | `desktop_app.py`, `theme.py`, `ui_components.py`, `AccessEase.pyw`, `assets/` | • Native Tkinter Canvas layout with custom `draw_rounded_rect()` card geometry.<br>• Deep Royal Purple (#482490) & Pastel Lilac (#F5F3FE) design system.<br>• Crash-free sequential tab state navigation and pastel blue dropdown styling. |
| **Student 4** | **Web Application, QA & Documentation Lead** | `app.py`, `Launch_Website.bat`, `AccessEase.bat`, `requirements.txt`, `README.md`, `USER_STORIES.md` | • Streamlit web deployment with dynamic session state bookmarks.<br>• Agile User Stories document (Word `.docx`, `.rtf`, Markdown) across 7 Epics.<br>• One-click batch launchers and cross-platform installation guide. |

### How to Combine Contributions (Git Workflow)
1. **Repository Setup**: One student initializes the Git repository on GitHub and invites the other 3 as collaborators.
2. **Feature Branching**:
   - Student 1 works on branch: `feature/landmarks-geodata`
   - Student 2 works on branch: `feature/haversine-logic-tests`
   - Student 3 works on branch: `feature/desktop-gui-canvas`
   - Student 4 works on branch: `feature/web-docs-launchers`
3. **Pull Requests & Code Review**: When a feature is complete, open a Pull Request (PR) to `main`. Every team member reviews the changes before merging to prevent code conflicts.

---

## 🛠️ Common Errors & Troubleshooting

1. **`'python' is not recognized as an internal or external command`**
   - **Fix**: Reinstall Python from [python.org](https://www.python.org/downloads/) and make sure to check the box **"Add Python to PATH"** on the very first installer screen.
2. **`ModuleNotFoundError: No module named 'streamlit'`**
   - **Fix**: Make sure you activated your virtual environment and ran `pip install -r requirements.txt`.
3. **`Script execution is disabled on this system` (PowerShell error)**
   - **Fix**: Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in your PowerShell terminal, then re-activate the virtual environment.
4. **Port 8501 is already in use**
   - **Fix**: Run `streamlit run app.py --server.port 8502` to start on a different port.
