"""
Skill Gap Prioritization and Personalized Learning Roadmap Generator.
"""

from typing import Dict, Any, List, Set

# Priority categorization heuristics based on domain importance
CORE_SKILL_PRIORITIES = {
    # High Priority Core Prerequisites
    "Programming Languages": "High",
    "Databases & Query Languages": "High",
    "Databases": "High",
    
    # Medium Priority Frameworks & Libraries
    "Machine Learning": "High",
    "Frontend Development": "Medium",
    "Backend Development": "High",
    "Data Science & Analytics": "High",
    "Natural Language Processing": "Medium",
    "Computer Vision": "Medium",
    "Computer Science Core": "High",
    
    # Tooling / Infrastructure / Cloud
    "DevOps & Cloud": "Medium",
    "Developer Tools": "Medium",
    "Data Engineering": "Medium",
    "Software Architecture": "Medium",
    "Software Engineering": "Medium",
    "System & OS": "Low"
}

PROJECT_SUGGESTIONS = {
    "Docker": "Containerize a multi-container application with Docker Compose and publish image to Docker Hub.",
    "Kubernetes": "Deploy a microservice cluster with ConfigMaps, persistent volumes, and ingress routing.",
    "AWS": "Host an API with EC2/Lambda, S3 storage buckets, and RDS PostgreSQL database.",
    "FastAPI": "Build an asynchronous CRUD REST API with JWT authentication and Pydantic validation.",
    "React": "Create a responsive single-page dashboard with client-side state management and REST API hooks.",
    "Next.js": "Build a server-side rendered web app with dynamic routing and optimized SEO performance.",
    "SQL": "Design a relational schema with foreign keys, indexing, and complex analytical aggregate queries.",
    "PostgreSQL": "Implement transactional relational database storage with optimized queries and connection pooling.",
    "Scikit-learn": "Train and cross-validate supervised regression and classification models on real-world datasets.",
    "PyTorch": "Implement a custom deep neural network training loop with loss functions and backpropagation.",
    "TensorFlow": "Train a convolutional neural network (CNN) for image recognition with data augmentation.",
    "Power BI": "Build an interactive multi-page business KPI dashboard with DAX calculated columns.",
    "Tableau": "Create visual storyboards analyzing customer cohort retention and sales breakdown.",
    "CI/CD": "Set up a GitHub Actions workflow with automated unit testing and build verification.",
    "Git": "Practice branching workflows, pull requests, resolving merge conflicts, and tagging releases.",
    "Redis": "Implement caching layer for high-latency database queries with TTL invalidation.",
    "Kafka": "Build an event-driven pub-sub producer and consumer pipeline for streaming message logs.",
    "REST API": "Design and document OpenAPI/Swagger specification for a multi-endpoint RESTful service."
}

class RoadmapGenerator:
    def __init__(self):
        pass

    def prioritize_skills(self, missing_skills: List[Dict[str, Any]], target_role: str = "") -> List[Dict[str, Any]]:
        """
        Assigns High, Medium, or Low priority to each missing skill based on category and target role.
        """
        prioritized = []

        for skill in missing_skills:
            name = skill["name"]
            category = skill.get("category", "General")

            # Determine base priority
            priority = CORE_SKILL_PRIORITIES.get(category, "Medium")

            # Contextual priority adjustments for target roles
            if "Data" in target_role or "ML" in target_role:
                if name in ["SQL", "Python", "Pandas", "Scikit-learn", "Statistics"]:
                    priority = "High"
            elif "Backend" in target_role or "Python Developer" in target_role:
                if name in ["SQL", "FastAPI", "Django", "REST API", "PostgreSQL", "Docker"]:
                    priority = "High"
            elif "Frontend" in target_role:
                if name in ["React", "TypeScript", "JavaScript", "HTML5", "CSS3", "Tailwind CSS"]:
                    priority = "High"
            elif "DevOps" in target_role:
                if name in ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"]:
                    priority = "High"

            # Assign suggested milestone project
            suggestion = PROJECT_SUGGESTIONS.get(
                name,
                f"Complete a focused tutorial and build a mini-project demonstrating practical use of {name}."
            )

            # Estimated learning duration
            est_duration = "1-2 weeks" if priority == "High" else "3-5 days"

            prioritized.append({
                "name": name,
                "category": category,
                "priority": priority,
                "estimated_time": est_duration,
                "project_milestone": suggestion,
                "rationale": f"{name} is a key requirement for {category} workflows in {target_role or 'this role'}."
            })

        # Sort order: High -> Medium -> Low
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        prioritized.sort(key=lambda x: (priority_order.get(x["priority"], 3), x["name"]))
        return prioritized

    def generate_roadmap(
        self,
        current_skills: List[str],
        missing_skills: List[Dict[str, Any]],
        target_role: str = "Target Role",
        overall_match_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Constructs a phased step-by-step roadmap for bridging candidate skill gaps.
        """
        prioritized_gaps = self.prioritize_skills(missing_skills, target_role)

        high_priority = [s for s in prioritized_gaps if s["priority"] == "High"]
        medium_priority = [s for s in prioritized_gaps if s["priority"] == "Medium"]
        low_priority = [s for s in prioritized_gaps if s["priority"] == "Low"]

        steps = []
        step_idx = 1

        # Step 0: Foundation / Current
        steps.append({
            "step": step_idx,
            "phase_title": "Current Foundation",
            "description": "Skills currently demonstrated in your resume.",
            "skills": current_skills[:10],
            "status": "completed",
            "action_item": "Consolidate portfolio repos with clear READMEs and live demos."
        })
        step_idx += 1

        # Phase 1: High Priority Critical Gaps
        if high_priority:
            steps.append({
                "step": step_idx,
                "phase_title": "Phase 1: High-Impact Core Skills",
                "description": "Master core technologies directly required for this target role.",
                "skills": [s["name"] for s in high_priority],
                "status": "pending",
                "action_item": "Build a dedicated capstone project integrating these essential tools.",
                "milestones": [s["project_milestone"] for s in high_priority[:3]]
            })
            step_idx += 1

        # Phase 2: Medium Priority Ecosystem & Tooling
        if medium_priority:
            steps.append({
                "step": step_idx,
                "phase_title": "Phase 2: Ecosystem & Modern Tooling",
                "description": "Broaden proficiency with complementary frameworks and development tooling.",
                "skills": [s["name"] for s in medium_priority],
                "status": "pending",
                "action_item": "Integrate CI/CD, testing, or containerization into your existing projects.",
                "milestones": [s["project_milestone"] for s in medium_priority[:3]]
            })
            step_idx += 1

        # Phase 3: Low Priority / Bonus
        if low_priority:
            steps.append({
                "step": step_idx,
                "phase_title": "Phase 3: Differentiator Skills",
                "description": "Secondary skills and cloud infrastructure to stand out among applicants.",
                "skills": [s["name"] for s in low_priority],
                "status": "pending",
                "action_item": "Deploy applications to cloud platforms and publish technical blog posts."
            })
            step_idx += 1

        # Final Goal
        steps.append({
            "step": step_idx,
            "phase_title": f"Goal: {target_role or 'Job-Ready Profile'}",
            "description": "Achieve 85%+ resume alignment and prepare for technical interviews.",
            "skills": [],
            "status": "target",
            "action_item": "Conduct mock technical interviews and tailor resume bullet points with quantifiable impact metrics."
        })

        return {
            "target_role": target_role,
            "overall_match_score": overall_match_score,
            "total_gaps": len(prioritized_gaps),
            "high_priority_count": len(high_priority),
            "medium_priority_count": len(medium_priority),
            "low_priority_count": len(low_priority),
            "prioritized_skills": prioritized_gaps,
            "roadmap_steps": steps
        }

# Global singleton instance
roadmap_generator = RoadmapGenerator()
