"""
Generate a diverse and realistic dataset for training resume role classification models.
Covers 8 key job roles with realistic combinations of skills, experience, project bullet points, and education text.
"""

import csv
import random
from pathlib import Path

# Seed for reproducibility
random.seed(42)

ROLES = {
    "Data Analyst": {
        "skills": [
            "SQL", "MySQL", "PostgreSQL", "Power BI", "Tableau", "Excel", "Advanced Excel",
            "VLOOKUP", "Pivot Tables", "Python", "Pandas", "NumPy", "Matplotlib", "Seaborn",
            "Data Visualization", "Data Cleaning", "EDA", "Statistical Analysis", "Business Intelligence",
            "Dashboarding", "Reporting", "ETL", "KPI Tracking", "A/B Testing"
        ],
        "project_templates": [
            "Analyzed customer churn trends using SQL and built interactive Power BI executive dashboards reducing report generation time by 40%.",
            "Conducted exploratory data analysis on sales datasets using Python and Pandas; extracted key revenue drivers and presented findings via Tableau.",
            "Designed automated ETL pipelines to extract data from MySQL and generate weekly business KPI reports in Excel.",
            "Performed statistical hypothesis testing and cohort analysis on e-commerce transaction data to optimize conversion funnels.",
            "Developed financial forecasting dashboards using Power BI and DAX measures for quarterly performance reviews."
        ],
        "summaries": [
            "Detail-oriented Data Analyst skilled in SQL, Power BI, and Python with a strong background in exploratory data analysis and business intelligence reporting.",
            "Aspiring Data Analyst with hands-on experience in statistical analysis, data cleaning with Pandas, and building interactive Tableau dashboards.",
            "Analytical thinker with expertise in relational databases, SQL querying, spreadsheet modeling, and translating raw data into actionable business insights."
        ]
    },
    "Data Scientist": {
        "skills": [
            "Python", "R", "Pandas", "NumPy", "Scikit-learn", "SciPy", "Statistics", "Probability",
            "Machine Learning", "Linear Regression", "Logistic Regression", "Random Forest", "XGBoost",
            "Hypothesis Testing", "Data Mining", "Feature Engineering", "Matplotlib", "Seaborn", "Jupyter", "SQL"
        ],
        "project_templates": [
            "Built predictive customer lifetime value models using Scikit-learn Random Forest and XGBoost with 89% precision.",
            "Engineered end-to-end data science pipelines from data ingestion and cleaning to feature selection and cross-validation.",
            "Implemented logistic regression and decision tree classifiers to predict loan default probabilities on credit datasets.",
            "Conducted multivariate statistical analysis and clustering algorithms (K-Means, PCA) to segment customer behavior patterns.",
            "Applied natural language processing techniques with TF-IDF and Naive Bayes to classify customer sentiment."
        ],
        "summaries": [
            "Data Scientist passionate about extracting predictive insights from complex datasets using Machine Learning, statistics, and Python.",
            "Quantitative Data Scientist with solid foundation in mathematical modeling, statistical hypothesis testing, and Scikit-learn predictive pipelines.",
            "Data Science graduate proficient in Python, machine learning algorithms, exploratory analysis, and data-driven problem solving."
        ]
    },
    "ML Engineer": {
        "skills": [
            "Python", "PyTorch", "TensorFlow", "Keras", "Deep Learning", "CNN", "RNN", "Transformers",
            "Hugging Face", "BERT", "Scikit-learn", "OpenCV", "MLOps", "Docker", "FastAPI",
            "Model Deployment", "Git", "NumPy", "CUDA", "LLM", "Computer Vision", "NLP"
        ],
        "project_templates": [
            "Trained and fine-tuned BERT transformer models with Hugging Face and PyTorch for multi-label text classification achieving 94% F1-score.",
            "Built real-time computer vision object detection pipeline using OpenCV and YOLOv8 with FastAPI inference microservice.",
            "Containerized deep learning models using Docker and deployed scalable REST inference APIs for production workloads.",
            "Implemented end-to-end MLOps pipeline for model tracking, hyperparameter tuning, and automated deployment.",
            "Developed convolutional neural network (CNN) architectures in TensorFlow/Keras for medical image classification."
        ],
        "summaries": [
            "Machine Learning Engineer specializing in Deep Learning, PyTorch, Hugging Face transformers, and containerized model deployment with FastAPI.",
            "ML Engineer experienced in computer vision, NLP models, distributed model training, and building scalable ML inference pipelines.",
            "AI/ML practitioner with strong expertise in deep neural networks, Python, PyTorch, and deploying machine learning models into production."
        ]
    },
    "Python Developer": {
        "skills": [
            "Python", "FastAPI", "Flask", "Django", "SQL", "PostgreSQL", "SQLite", "REST API",
            "Pytest", "Git", "Celery", "Redis", "OOP", "Data Structures", "Docker",
            "Web Scraping", "BeautifulSoup", "Asyncio", "Unit Testing", "Microservices"
        ],
        "project_templates": [
            "Developed high-performance asynchronous RESTful APIs using FastAPI and PostgreSQL with Pydantic schema validation and JWT authentication.",
            "Architected full-featured web applications using Django ORM and Celery background workers with Redis caching.",
            "Built automated web scraping and data aggregation pipelines using Python, BeautifulSoup, and Requests with rate limiting.",
            "Wrote comprehensive unit and integration test suites using Pytest achieving 90%+ code coverage across backend microservices.",
            "Implemented secure token-based user authentication, role-based access control, and database migrations using Alembic."
        ],
        "summaries": [
            "Backend Python Developer with expertise in building scalable REST APIs using FastAPI, Django, PostgreSQL, and writing clean asynchronous code.",
            "Python Software Engineer passionate about clean code architecture, database optimization, Celery task queues, and Pytest testing.",
            "Versatile Python Developer with hands-on experience in backend web development, API integrations, and database design."
        ]
    },
    "Frontend Developer": {
        "skills": [
            "JavaScript", "TypeScript", "React", "Next.js", "Vue.js", "HTML5", "CSS3", "Tailwind CSS",
            "Redux", "Redux Toolkit", "REST API", "Responsive Web Design", "SASS", "Webpack", "Vite",
            "Git", "UI/UX", "Axios", "Jest", "Figma"
        ],
        "project_templates": [
            "Designed and built responsive single-page web applications using React, TypeScript, and Tailwind CSS with dynamic routing.",
            "Implemented complex global state management and caching using Redux Toolkit and React Query for asynchronous API calls.",
            "Built server-side rendered (SSR) web portals using Next.js, optimizing Core Web Vitals and achieving 98+ Lighthouse performance score.",
            "Created reusable component libraries in React adhering to accessibility standards (a11y) and responsive design principles.",
            "Integrated backend RESTful API endpoints and WebSocket streams for real-time live data visualization dashboards."
        ],
        "summaries": [
            "Creative Frontend Developer passionate about building sleek, high-performance web applications using React, TypeScript, and Tailwind CSS.",
            "Frontend Engineer with proven track record in responsive design, modern state management (Redux/Zustand), and component-driven architecture.",
            "User-focused UI Developer specializing in modern JavaScript (ES6+), React.js ecosystem, and crafting seamless interactive experiences."
        ]
    },
    "Backend Developer": {
        "skills": [
            "Java", "Spring Boot", "Spring MVC", "Microservices", "REST API", "SQL", "PostgreSQL",
            "MySQL", "Hibernate", "JPA", "Docker", "Git", "Maven", "Kafka", "Redis",
            "Distributed Systems", "JUnit", "Data Structures", "Design Patterns", "CI/CD"
        ],
        "project_templates": [
            "Architected distributed microservices using Java 17 and Spring Boot with Spring Cloud Gateway and Eureka service discovery.",
            "Designed high-throughput message streaming pipelines using Apache Kafka and Spring Kafka consumers for asynchronous event processing.",
            "Optimized relational database schemas and complex SQL queries in PostgreSQL using JPA/Hibernate, reducing query latency by 35%.",
            "Implemented distributed caching with Redis to reduce database read load on high-traffic e-commerce endpoints.",
            "Developed secure RESTful web services with OAuth2, JWT authentication, and automated testing via JUnit 5 and Mockito."
        ],
        "summaries": [
            "Backend Engineer specializing in Java, Spring Boot microservices, Kafka event streaming, and resilient relational database design.",
            "Dedicated Backend Developer with strong knowledge of distributed systems, REST API architecture, Redis caching, and Clean Code.",
            "Software Developer with solid expertise in Java enterprise ecosystem, microservices architecture, and high-performance backend systems."
        ]
    },
    "Full Stack Developer": {
        "skills": [
            "JavaScript", "TypeScript", "React", "Node.js", "Express.js", "MongoDB", "PostgreSQL",
            "HTML5", "CSS3", "Tailwind CSS", "REST API", "Git", "Docker", "Next.js", "Redux",
            "GraphQL", "Prisma", "Full Stack Web Development", "MERN Stack"
        ],
        "project_templates": [
            "Built end-to-end full stack web applications using React, Node.js, Express, and MongoDB with secure JWT authorization.",
            "Developed e-commerce platform using Next.js, TypeScript, PostgreSQL, and Stripe payment gateway with Prisma ORM.",
            "Engineered real-time collaborative workspace with React frontend, Node.js Socket.io backend, and Redis pub/sub.",
            "Designed REST and GraphQL APIs connecting React client applications to relational databases with comprehensive input validation.",
            "Containerized full stack applications with Docker and Docker Compose for streamlined local development and staging deployments."
        ],
        "summaries": [
            "Versatile Full Stack Developer proficient in React, Node.js, Express, TypeScript, and relational/NoSQL databases.",
            "MERN Stack Developer with end-to-end experience in architecting modern responsive user interfaces and robust backend APIs.",
            "Full Stack Software Engineer skilled in modern web technologies, RESTful architectures, and building production-ready web apps."
        ]
    },
    "DevOps Engineer": {
        "skills": [
            "Docker", "Kubernetes", "AWS", "EC2", "S3", "Lambda", "Terraform", "CI/CD",
            "GitHub Actions", "Jenkins", "Linux", "Bash", "Shell Scripting", "Ansible",
            "Prometheus", "Grafana", "Git", "Nginx", "Infrastructure as Code", "Cloud Architecture"
        ],
        "project_templates": [
            "Automated multi-stage CI/CD deployment pipelines using GitHub Actions and Docker, reducing deployment cycle times from hours to minutes.",
            "Managed Kubernetes (EKS/k8s) clusters for container orchestration, auto-scaling, and zero-downtime rolling updates.",
            "Provisioned secure cloud infrastructure on AWS using Terraform (Infrastructure as Code) including VPCs, EC2, S3, and RDS.",
            "Implemented infrastructure monitoring, alerting, and logging systems using Prometheus, Grafana, and ELK Stack.",
            "Hardened Linux production servers, configured Nginx reverse proxies, and automated configuration management using Ansible."
        ],
        "summaries": [
            "DevOps Engineer skilled in AWS cloud infrastructure, Docker containerization, Kubernetes orchestration, and automated CI/CD pipelines.",
            "Cloud & DevOps practitioner with strong focus on Infrastructure as Code (Terraform), Linux systems administration, and monitoring.",
            "Site Reliability & DevOps Engineer experienced in modern cloud platforms, container lifecycle management, and pipeline automation."
        ]
    }
}

EDUCATION_OPTIONS = [
    "Bachelor of Technology in Computer Science and Engineering",
    "Bachelor of Science in Information Technology",
    "Bachelor of Engineering in Data Science",
    "Master of Science in Computer Science",
    "Bachelor of Computer Applications (BCA)",
    "B.Tech in Artificial Intelligence and Data Engineering"
]

def generate_sample(role: str) -> str:
    role_data = ROLES[role]
    
    # Select summary
    summary = random.choice(role_data["summaries"])
    
    # Select subset of core skills + maybe 1-2 cross skills
    num_skills = random.randint(6, 12)
    selected_skills = random.sample(role_data["skills"], min(num_skills, len(role_data["skills"])))
    
    # 20% chance to have a cross-discipline skill (e.g. Git, Linux, Docker)
    common_skills = ["Git", "Linux", "Data Structures", "Unit Testing", "Agile", "Problem Solving"]
    for cs in random.sample(common_skills, random.randint(1, 3)):
        if cs not in selected_skills:
            selected_skills.append(cs)
            
    # Select 2-3 project templates
    num_projects = random.randint(2, 3)
    projects = random.sample(role_data["project_templates"], num_projects)
    
    # Select education
    education = random.choice(EDUCATION_OPTIONS)
    
    # Format resume text
    resume_text = f"""
Summary:
{summary}

Technical Skills:
{", ".join(selected_skills)}

Projects & Experience:
- {projects[0]}
- {projects[1]}
{f"- {projects[2]}" if len(projects) > 2 else ""}

Education:
{education}
""".strip()
    
    return resume_text

def main():
    output_dir = Path("backend/data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "resume_role_dataset.csv"
    
    # Generate 60 samples per role = 480 diverse samples
    samples_per_role = 60
    records = []
    
    for role in ROLES:
        for _ in range(samples_per_role):
            text = generate_sample(role)
            records.append({"resume_text": text, "role": role})
            
    random.shuffle(records)
    
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["resume_text", "role"])
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Successfully generated {len(records)} resume samples across {len(ROLES)} roles at {output_csv}")

if __name__ == "__main__":
    main()
