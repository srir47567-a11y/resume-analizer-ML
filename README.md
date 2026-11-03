# Resume Analyzer ML

A full-stack application for analyzing resumes using machine learning. It parses resume files, extracts key information, and matches candidates against job descriptions.

> **Project status:** Work in progress. Features and structure described below are the intended design and may not all be present yet.

---

## 📖 Overview

Resume Analyzer ML aims to provide an end-to-end solution for resume analysis: a Python backend with ML models for parsing and matching, a simple web frontend, and a test suite.

## ✨ Planned / In-Progress Features

- **Resume Parsing** – Extract text and structured data from PDF/DOCX resumes
- **ML-based Matching** – Compare resumes against job descriptions
- **Scoring & Ranking** – Assign relevance scores to candidates
- **Web Interface** – Upload resumes and view results in the browser
- **REST API** – Programmatic access to analysis
- **Test Coverage** – Unit tests for parser, matcher, and ML components

## 🛠️ Tech Stack

| Layer    | Technology                              |
|----------|-----------------------------------------|
| Backend  | Python                                  |
| Frontend | HTML, CSS, JavaScript                   |
| ML       | Python (see `requirements.txt`)         |
| Testing  | pytest                                  |

## 📁 Project Structure
resume-analizer-ML/
├── backend/
│ ├── app/
│ │ ├── api/ # API routes
│ │ ├── ml/ # Machine learning logic
│ │ ├── models/ # Data models
│ │ ├── services/ # Business logic
│ │ └── utils/ # Helper functions
│ ├── data/ # Datasets
│ ├── main.py # App entry point
│ └── requirements.txt # Python dependencies
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── app.js
├── tests/
│ ├── test_matcher.py
│ ├── test_ml.py
│ └── test_parser.py
├── sample_resumes/ # Example resumes
├── run.py # Start backend server
├── start.bat # Windows quick-start
├── pytest.ini # Pytest config
└── README.md



## ⚙️ Prerequisites

- Python 3.8+
- pip
- Git

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/srir47567-a11y/resume-analizer-ML.git
   cd resume-analizer-ML

2. Create and activate a virtual environment


    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

3. Install backend dependencies

    pip install -r backend/requirements.txt

▶️ Running the Application
    Backend

    python run.py

On Windows you can also use:
    start.bat
    Frontend

Open frontend/index.html in a browser, or serve it:
    cd frontend
    python -m http.server 8000
    Then visit http://localhost:8000

📝 Usage
1. Start the backend server.
2. Open the frontend in your browser.
3. Upload a resume (PDF/DOCX).
4. Optionally provide a job description.
5. View the extracted data, score, and recommendations.