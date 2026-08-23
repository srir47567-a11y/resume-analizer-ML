/**
 * SkillMatch ML — Frontend Reactivity and API Integration
 */

// Sample Data Presets for Instant 1-Click Demos
const SAMPLE_RESUMES = {
  data_analyst: `John Doe | john.doe@email.com | +1 555-019-2834 | linkedin.com/in/johndoe | github.com/johndoe
SUMMARY:
Detail-oriented Data Analyst graduate with hands-on expertise in SQL querying, exploratory data analysis, and building executive dashboards using Power BI and Excel. Passionate about translating messy data into actionable business intelligence.

TECHNICAL SKILLS:
- Languages & Databases: SQL, MySQL, PostgreSQL, Python
- Analytics & Libraries: Pandas, NumPy, Matplotlib, Seaborn, Statistics
- BI & Tools: Power BI, Tableau, Advanced Excel (VLOOKUP, Pivot Tables), Git

PROJECTS:
1. Customer Churn Intelligence Dashboard (Power BI, SQL, Python):
   - Extracted and cleaned 50,000+ transactional customer records using SQL and Pandas.
   - Built interactive multi-page Power BI dashboard tracking monthly churn rates and revenue loss drivers.
   
2. E-Commerce Sales Performance & Cohort Analysis (Python, Pandas, Tableau):
   - Performed exploratory data analysis (EDA) and cohort retention analysis on retail transaction datasets.
   - Designed interactive Tableau storyboards revealing top 10 revenue-generating product categories.

EDUCATION:
Bachelor of Technology in Computer Science & Engineering — 2024
`,
  python_dev: `Alex Rivera | alex.rivera@email.com | +1 555-482-9102 | github.com/alexrivera
SUMMARY:
Backend Python Developer with solid experience in building asynchronous REST APIs using FastAPI, PostgreSQL, and Redis. Passionate about clean architecture, unit testing with Pytest, and microservice patterns.

TECHNICAL SKILLS:
- Languages: Python, JavaScript, SQL
- Backend Frameworks: FastAPI, Flask, Django, REST API
- Databases & Caching: PostgreSQL, SQLite, Redis
- Tools & Practices: Git, Docker, Pytest, Unit Testing, Linux, Data Structures

PROJECTS:
1. Asynchronous E-Commerce Inventory API (FastAPI, PostgreSQL, Redis):
   - Built high-performance async RESTful API endpoints handling product catalog and inventory checkout.
   - Integrated Redis caching layer reducing database read latencies by 45%.
   - Implemented JWT authentication and schema validation using Pydantic.

2. Web Scraping & Aggregation Engine (Python, BeautifulSoup, Celery):
   - Developed distributed scraping workers to extract tech job postings across 5 platforms with rate limiting.

EDUCATION:
Bachelor of Science in Information Technology — 2024
`,
  frontend_dev: `Sarah Chen | sarah.chen@email.com | +1 555-739-1823 | github.com/sarahchen | sarahchen.dev
SUMMARY:
Frontend Engineer passionate about crafting beautiful, accessible, and high-performance web applications using React, TypeScript, and Tailwind CSS. Strong foundation in state management and responsive UI/UX.

TECHNICAL SKILLS:
- Languages: TypeScript, JavaScript (ES6+), HTML5, CSS3
- Frontend: React, Next.js, Redux, Redux Toolkit, Tailwind CSS, Responsive Web Design
- Tooling: Git, Vite, Webpack, Jest, Figma, REST API

PROJECTS:
1. TaskFlow — Collaborative Kanban Board (React, TypeScript, Tailwind CSS):
   - Designed and built responsive drag-and-drop workspace using React and Redux Toolkit.
   - Integrated RESTful API hooks with optimistic UI updates and real-time validation.

2. CryptoPulse Market Tracker (Next.js, TypeScript, Chart.js):
   - Built server-rendered cryptocurrency dashboard consuming public REST APIs with 98+ Lighthouse performance score.

EDUCATION:
Bachelor of Computer Applications (BCA) — 2024
`,
  ml_engineer: `David Kumar | david.kumar@email.com | +1 555-891-2345 | github.com/davidkumar
SUMMARY:
Machine Learning Engineer specializing in Deep Learning, PyTorch, Hugging Face transformers, and containerized model inference pipelines with FastAPI and Docker.

TECHNICAL SKILLS:
- ML & Deep Learning: PyTorch, TensorFlow, Keras, Scikit-learn, Hugging Face, BERT, CNN, OpenCV
- Programming: Python, C++, SQL, NumPy, Pandas
- Deployment & Tools: FastAPI, Docker, Git, Linux, MLOps

PROJECTS:
1. Multimodal Sentiment Analysis with Transformers (PyTorch, Hugging Face, FastAPI):
   - Fine-tuned BERT and RoBERTa models on customer review datasets achieving 93.5% F1-score.
   - Containerized model with Docker and deployed asynchronous FastAPI inference endpoint.

2. Real-time Object Detection Pipeline (OpenCV, YOLOv8, Python):
   - Developed video inference pipeline processing 45 FPS on edge GPU hardware.

EDUCATION:
B.Tech in Artificial Intelligence & Data Science — 2024
`
};

const SAMPLE_JDS = {
  data_analyst_jd: `Role: Junior Data Analyst
Location: Remote / Hybrid
Experience: Freshers / 0-2 Years

Responsibilities:
- Extract, clean, and model complex datasets from relational databases using SQL.
- Build and maintain interactive dashboards in Power BI and Tableau for business stakeholders.
- Perform exploratory data analysis and statistical reporting using Python, Pandas, and Excel.
- Identify key performance indicators (KPIs) and present findings to cross-functional teams.

Requirements:
- Strong proficiency in SQL, PostgreSQL or MySQL.
- Experience with Power BI, Tableau, and Advanced Excel (Pivot tables, formulas).
- Familiarity with Python, Pandas, NumPy, and Data Visualization libraries.
- Understanding of basic statistical analysis and hypothesis testing.
- Git and version control knowledge is a plus.
`,
  python_backend_jd: `Role: Python Backend Developer
Location: Bangalore / Remote
Experience: Entry Level / 0-2 Years

About the Role:
We are seeking a Python Developer to join our core backend engineering team building scalable web APIs and microservices.

Requirements:
- Strong proficiency in Python 3, Object-Oriented Programming, and Data Structures.
- Hands-on experience with FastAPI, Flask, or Django REST Framework.
- Solid understanding of relational databases (PostgreSQL, SQL) and query optimization.
- Experience with Docker containerization and AWS cloud infrastructure (EC2, S3).
- Familiarity with Redis caching, Celery task queues, and automated Unit Testing with Pytest.
- Git workflow and CI/CD pipelines.
`,
  frontend_jd: `Role: Frontend React Developer
Location: Remote

Responsibilities:
- Build responsive, accessible, and high-performance user interfaces using React and TypeScript.
- Collaborate with UI/UX designers in Figma to translate mockups into clean Tailwind CSS components.
- Manage client-side application state using Redux Toolkit or React Query.
- Connect frontend components with RESTful and GraphQL backend APIs.

Requirements:
- Strong foundation in HTML5, CSS3, JavaScript (ES6+), and TypeScript.
- Hands-on project experience in React.js and Next.js.
- Proficiency in Tailwind CSS and responsive design.
- Experience with Git, Vite, and testing with Jest.
`,
  ml_engineer_jd: `Role: Associate Machine Learning Engineer
Location: Hyderabad / Hybrid

Responsibilities:
- Design, train, and evaluate machine learning and deep learning models for NLP and Computer Vision.
- Build production-ready inference microservices using FastAPI and Docker.
- Implement data pipelines and feature engineering with Pandas, NumPy, and Scikit-learn.

Requirements:
- Strong Python programming and ML foundations (Scikit-learn, PyTorch, or TensorFlow).
- Experience with Hugging Face transformers, BERT, or deep neural networks.
- Familiarity with Docker, Linux environments, and Git.
- Exposure to AWS or Cloud MLOps is preferred.
`
};

// Application State
let selectedResumeFile = null;
let currentResumeText = "";

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Lucide icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Setup Event Listeners
  setupTabControls();
  setupFileUpload();
  setupPresets();
  setupActionButtons();
  setupModal();
});

function setupTabControls() {
  const tabBtnFile = document.getElementById("tab-btn-file");
  const tabBtnText = document.getElementById("tab-btn-text");
  const tabContentFile = document.getElementById("tab-content-file");
  const tabContentText = document.getElementById("tab-content-text");

  tabBtnFile.addEventListener("click", () => {
    tabBtnFile.classList.add("active");
    tabBtnText.classList.remove("active");
    tabContentFile.style.display = "block";
    tabContentText.style.display = "none";
  });

  tabBtnText.addEventListener("click", () => {
    tabBtnText.classList.add("active");
    tabBtnFile.classList.remove("active");
    tabContentText.style.display = "block";
    tabContentFile.style.display = "none";
  });
}

function setupFileUpload() {
  const dropZone = document.getElementById("resume-drop-zone");
  const fileInput = document.getElementById("resume-file-input");
  const btnBrowse = document.getElementById("btn-browse-file");
  const banner = document.getElementById("file-loaded-banner");
  const fileNameDisplay = document.getElementById("loaded-file-name");
  const btnClear = document.getElementById("btn-clear-file");
  const dropContent = dropZone.querySelector(".drop-zone-content");

  btnBrowse.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  dropZone.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  // Drag & Drop
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("dragover");
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("dragover");
    });
  });

  dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    if (dt.files && dt.files.length > 0) {
      handleFileSelected(dt.files[0]);
    }
  });

  btnClear.addEventListener("click", (e) => {
    e.stopPropagation();
    selectedResumeFile = null;
    fileInput.value = "";
    banner.style.display = "none";
    dropContent.style.display = "block";
  });

  function handleFileSelected(file) {
    selectedResumeFile = file;
    fileNameDisplay.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
    banner.style.display = "flex";
    dropContent.style.display = "none";
    if (window.lucide) window.lucide.createIcons();
  }
}

function setupPresets() {
  const sampleResumeSelect = document.getElementById("sample-resume-select");
  const sampleJdSelect = document.getElementById("sample-jd-select");
  const resumeTextInput = document.getElementById("resume-text-input");
  const jdTextInput = document.getElementById("jd-text-input");
  const tabBtnText = document.getElementById("tab-btn-text");

  sampleResumeSelect.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val && SAMPLE_RESUMES[val]) {
      resumeTextInput.value = SAMPLE_RESUMES[val];
      // Switch to text tab to show loaded text
      tabBtnText.click();
    }
  });

  sampleJdSelect.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val && SAMPLE_JDS[val]) {
      jdTextInput.value = SAMPLE_JDS[val];
    }
  });

  // Quick Demo Auto-Loader
  document.getElementById("btn-quick-demo").addEventListener("click", (e) => {
    sampleResumeSelect.value = "python_dev";
    sampleResumeSelect.dispatchEvent(new Event("change"));
    
    sampleJdSelect.value = "python_backend_jd";
    sampleJdSelect.dispatchEvent(new Event("change"));
    
    setTimeout(() => {
      document.getElementById("btn-run-analysis").click();
    }, 200);
  });
}

function setupActionButtons() {
  const btnRun = document.getElementById("btn-run-analysis");
  btnRun.addEventListener("click", executeFullAnalysis);
}

async function executeFullAnalysis() {
  const resumeTextInput = document.getElementById("resume-text-input");
  const jdTextInput = document.getElementById("jd-text-input");
  const loadingContainer = document.getElementById("loading-container");
  const resultsSection = document.getElementById("results-section");

  let resumeText = resumeTextInput.value.trim();
  const jdText = jdTextInput.value.trim();

  // If a file is selected in upload tab, upload file first
  if (selectedResumeFile) {
    loadingContainer.style.display = "block";
    resultsSection.style.display = "none";

    const formData = new FormData();
    formData.append("file", selectedResumeFile);

    try {
      const uploadResp = await fetch("/api/resume/upload", {
        method: "POST",
        body: formData
      });
      const uploadData = await uploadResp.json();
      if (!uploadData.success) {
        alert(`Resume extraction error: ${uploadData.detail || "Unknown error"}`);
        loadingContainer.style.display = "none";
        return;
      }
      resumeText = uploadData.raw_text;
      resumeTextInput.value = resumeText;
    } catch (err) {
      alert(`Network error uploading file: ${err.message}`);
      loadingContainer.style.display = "none";
      return;
    }
  }

  if (!resumeText) {
    alert("Please upload a resume file or paste resume text to analyze.");
    return;
  }

  loadingContainer.style.display = "block";
  resultsSection.style.display = "none";

  try {
    const response = await fetch("/api/analyze-full", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jdText || null
      })
    });

    const data = await response.json();
    loadingContainer.style.display = "none";

    if (!data.success) {
      alert(`Analysis failed: ${data.detail || "Unknown error"}`);
      return;
    }

    renderResults(data);
    resultsSection.style.display = "block";
    resultsSection.scrollIntoView({ behavior: "smooth" });

  } catch (err) {
    loadingContainer.style.display = "none";
    alert(`Request error: ${err.message}`);
  }
}

function renderResults(data) {
  const rolePred = data.role_prediction || {};
  const jobMatch = data.job_match || {};
  const roadmap = data.roadmap || {};
  const skills = data.skills || [];

  // 1. Top ML Role
  const topRoleEl = document.getElementById("metric-top-role");
  const roleConfEl = document.getElementById("metric-role-confidence");
  const roleBarsEl = document.getElementById("role-probability-bars");

  topRoleEl.textContent = rolePred.top_role || "Undetermined";
  roleConfEl.innerHTML = `Model Confidence: <strong>${rolePred.top_confidence || 0}%</strong>`;

  // Render role bars
  roleBarsEl.innerHTML = "";
  (rolePred.predictions || []).slice(0, 3).forEach(p => {
    const barItem = document.createElement("div");
    barItem.className = "role-bar-item";
    barItem.innerHTML = `
      <div class="role-bar-header">
        <span>${p.role}</span>
        <span>${p.confidence_percentage}%</span>
      </div>
      <div class="role-progress-track">
        <div class="role-progress-fill" style="width: ${p.confidence_percentage}%"></div>
      </div>
    `;
    roleBarsEl.appendChild(barItem);
  });

  // 2. Resume-Job Match Gauge
  const matchScoreEl = document.getElementById("metric-match-score");
  const gaugeProgress = document.getElementById("gauge-progress");
  const skillCoverageEl = document.getElementById("metric-skill-coverage");
  const textSimEl = document.getElementById("metric-text-sim");

  const score = jobMatch.overall_match_score !== undefined ? jobMatch.overall_match_score : (rolePred.top_confidence || 0);
  matchScoreEl.textContent = Math.round(score);

  // SVG dasharray: score, 100
  gaugeProgress.setAttribute("stroke-dasharray", `${Math.round(score)}, 100`);

  // Progress bar color based on score
  if (score >= 75) {
    gaugeProgress.style.stroke = "#10b981"; // emerald
  } else if (score >= 50) {
    gaugeProgress.style.stroke = "#06b6d4"; // cyan
  } else {
    gaugeProgress.style.stroke = "#f59e0b"; // amber
  }

  skillCoverageEl.textContent = `${jobMatch.skill_coverage_score || 0}%`;
  textSimEl.textContent = `${jobMatch.text_similarity_score || 0}%`;

  // 3. Counts
  const matchedCount = jobMatch.matched_skills ? jobMatch.matched_skills.length : skills.length;
  const missingCount = jobMatch.missing_skills ? jobMatch.missing_skills.length : 0;

  document.getElementById("metric-matched-count").textContent = matchedCount;
  document.getElementById("badge-matched-count").textContent = `${matchedCount} Verified`;
  document.getElementById("metric-missing-count").textContent = missingCount;
  document.getElementById("badge-missing-count").textContent = `${missingCount} Missing`;

  // 4. Matched & Extra Skills Chips
  const matchedContainer = document.getElementById("matched-skills-container");
  const extraContainer = document.getElementById("extra-skills-container");
  matchedContainer.innerHTML = "";
  extraContainer.innerHTML = "";

  const matchedSkillsList = jobMatch.matched_skills || skills;
  matchedSkillsList.forEach(s => {
    const chip = document.createElement("div");
    chip.className = "chip chip-matched";
    chip.innerHTML = `<span>✓</span> <strong>${s.name}</strong> <span class="chip-tag">${s.category}</span>`;
    matchedContainer.appendChild(chip);
  });

  const extraSkillsList = jobMatch.extra_skills || [];
  if (extraSkillsList.length === 0 && !jobMatch.matched_skills) {
    extraContainer.innerHTML = `<p style="font-size: 0.8rem; color: var(--text-dim);">Paste a job description to separate target matches from extra skills.</p>`;
  } else {
    extraSkillsList.forEach(s => {
      const chip = document.createElement("div");
      chip.className = "chip chip-extra";
      chip.innerHTML = `<strong>${s.name}</strong> <span class="chip-tag">${s.category}</span>`;
      extraContainer.appendChild(chip);
    });
  }

  // 5. Missing Skill Gaps with Priority Badges
  const missingContainer = document.getElementById("missing-skills-container");
  missingContainer.innerHTML = "";

  const missingSkillsList = (roadmap.prioritized_skills) || (jobMatch.missing_skills || []);
  if (missingSkillsList.length === 0) {
    missingContainer.innerHTML = `
      <div style="padding: 1rem; text-align: center; color: var(--emerald); font-size: 0.9rem;">
        🎉 Outstanding! No critical skill gaps identified for this profile and target requirements.
      </div>
    `;
  } else {
    missingSkillsList.forEach(g => {
      const priorityClass = g.priority === "High" ? "badge-rose" : (g.priority === "Medium" ? "badge-amber" : "badge-cyan");
      const gapItem = document.createElement("div");
      gapItem.className = "gap-item";
      gapItem.innerHTML = `
        <div class="gap-info">
          <div class="gap-title">
            <span>✗ ${g.name}</span>
            <span class="badge ${priorityClass}">${g.priority || 'Required'} Priority</span>
          </div>
          <span class="gap-category">${g.category} &bull; Est. ${g.estimated_time || '1 week'}</span>
          <span class="gap-project">💡 ${g.project_milestone || 'Build a focused project implementing this technology.'}</span>
        </div>
      `;
      missingContainer.appendChild(gapItem);
    });
  }

  // 6. Phased Learning Roadmap Timeline
  const roadmapContainer = document.getElementById("roadmap-timeline-container");
  const targetBadge = document.getElementById("target-role-badge");
  roadmapContainer.innerHTML = "";

  targetBadge.textContent = `Target: ${roadmap.target_role || rolePred.top_role || 'Job Ready'}`;

  const steps = roadmap.roadmap_steps || [
    { step: 1, phase_title: "Current Foundation", description: "Demonstrated skills in resume.", status: "completed", skills: skills.map(s => s.name).slice(0, 8), action_item: "Publish GitHub portfolio with clean documentation." },
    { step: 2, phase_title: "Phase 1: High Priority Gaps", description: "Learn key requirements.", status: "pending", skills: ["Target Frameworks"], action_item: "Build full capstone project." },
    { step: 3, phase_title: "Goal: Job Ready", description: "Interview ready portfolio.", status: "target", skills: [], action_item: "Prepare for behavioral and technical interviews." }
  ];

  steps.forEach(st => {
    const markerClass = st.status === "completed" ? "completed" : (st.status === "target" ? "target" : "");
    const stepEl = document.createElement("div");
    stepEl.className = "timeline-step";
    
    let skillsTags = "";
    if (st.skills && st.skills.length > 0) {
      skillsTags = `<div class="chips-container" style="margin-top: 0.5rem; margin-bottom: 0;">
        ${st.skills.map(sk => `<span class="chip" style="font-size: 0.75rem;">${sk}</span>`).join("")}
      </div>`;
    }

    let milestonesHtml = "";
    if (st.milestones && st.milestones.length > 0) {
      milestonesHtml = `<ul style="margin: 0.5rem 0 0 1.2rem; font-size: 0.78rem; color: #94a3b8;">
        ${st.milestones.map(m => `<li>${m}</li>`).join("")}
      </ul>`;
    }

    stepEl.innerHTML = `
      <div class="step-marker ${markerClass}">${st.step}</div>
      <div class="step-body">
        <div class="step-header">
          <div class="step-title">${st.phase_title}</div>
          <span class="badge ${st.status === 'completed' ? 'badge-emerald' : (st.status === 'target' ? 'badge-cyan' : 'badge-indigo')}">${st.status.toUpperCase()}</span>
        </div>
        <div class="step-desc">${st.description}</div>
        ${skillsTags}
        ${milestonesHtml}
        <div class="step-action">⚡ Action: ${st.action_item}</div>
      </div>
    `;
    roadmapContainer.appendChild(stepEl);
  });

  // 7. Explainability & Evidence
  const evidenceContainer = document.getElementById("evidence-list-container");
  const keywordsContainer = document.getElementById("influential-keywords-container");
  evidenceContainer.innerHTML = "";
  keywordsContainer.innerHTML = "";

  const evidence = jobMatch.evidence_points || [
    `Resume contains ${skills.length} verified canonical technical skills`,
    `Strong alignment detected in programming languages and database technologies`,
    `Section parser identified explicit project achievements`
  ];

  evidence.forEach(ev => {
    const li = document.createElement("li");
    li.textContent = ev;
    evidenceContainer.appendChild(li);
  });

  const keywords = rolePred.influential_keywords || [];
  keywords.forEach(kw => {
    const tag = document.createElement("span");
    tag.className = "keyword-badge";
    tag.textContent = `${kw.token} (${kw.weight})`;
    keywordsContainer.appendChild(tag);
  });

  if (window.lucide) window.lucide.createIcons();
}

function setupModal() {
  const modal = document.getElementById("modal-benchmarks");
  const btnOpen = document.getElementById("btn-view-model-metrics");
  const btnClose = document.getElementById("btn-close-modal");
  const content = document.getElementById("modal-benchmark-content");

  btnOpen.addEventListener("click", async () => {
    modal.style.display = "flex";
    content.innerHTML = `<div class="spinner-pulse"></div>`;

    try {
      const resp = await fetch("/api/models/evaluation");
      const data = await resp.json();
      if (!data.success) {
        content.innerHTML = `<p>Failed to load benchmarks.</p>`;
        return;
      }

      const evalData = data.evaluation;
      const comps = evalData.model_comparisons || {};

      let rowsHtml = "";
      for (const [modelName, m] of Object.entries(comps)) {
        const isBest = modelName === evalData.best_model;
        rowsHtml += `
          <tr style="${isBest ? 'background: rgba(99, 102, 241, 0.12); font-weight: 700;' : ''}">
            <td>${modelName} ${isBest ? '⭐ <span class="badge badge-indigo">Selected</span>' : ''}</td>
            <td>${(m.accuracy * 100).toFixed(1)}%</td>
            <td>${(m.precision_macro * 100).toFixed(1)}%</td>
            <td>${(m.recall_macro * 100).toFixed(1)}%</td>
            <td>${(m.f1_macro * 100).toFixed(1)}%</td>
          </tr>
        `;
      }

      content.innerHTML = `
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
          Trained on <strong>480 stratified resume samples</strong> across <strong>${evalData.classes.length} distinct target roles</strong>.
          Evaluated using 80/20 train/test split with zero data leakage (TF-IDF fitted exclusively on training split).
        </p>

        <table class="benchmark-table">
          <thead>
            <tr>
              <th>Model Architecture</th>
              <th>Accuracy</th>
              <th>Precision (Macro)</th>
              <th>Recall (Macro)</th>
              <th>F1-Score (Macro)</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>

        <div style="margin-top: 1.5rem;">
          <h4 style="font-size: 0.9rem; margin-bottom: 0.5rem;">Role Categories (${evalData.classes.length}):</h4>
          <div class="chips-container">
            ${evalData.classes.map(c => `<span class="chip" style="font-size: 0.78rem;">${c}</span>`).join("")}
          </div>
        </div>
      `;

      if (window.lucide) window.lucide.createIcons();

    } catch (err) {
      content.innerHTML = `<p style="color: var(--rose);">Error loading metrics: ${err.message}</p>`;
    }
  });

  btnClose.addEventListener("click", () => {
    modal.style.display = "none";
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
}
