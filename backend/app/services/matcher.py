"""
Resume to Job Description Matcher Service.
Calculates TF-IDF Cosine Similarity, Skill Overlap, and Explainable Match Scores.
"""

from typing import Dict, Any, List, Set
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.app.services.skill_extractor import skill_extractor
from backend.app.ml.preprocess import normalize_for_nlp

class JobMatcher:
    def __init__(self):
        pass

    def calculate_text_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Computes cosine similarity between TF-IDF representations of resume and job description.
        Returns value between 0.0 and 100.0.
        """
        norm_resume = normalize_for_nlp(resume_text)
        norm_jd = normalize_for_nlp(jd_text)

        if not norm_resume or not norm_jd:
            return 0.0

        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        tfidf_matrix = vectorizer.fit_transform([norm_resume, norm_jd])

        # Cosine similarity between row 0 and row 1
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(sim) * 100.0, 1)

    def match(self, resume_text: str, jd_text: str, sections_dict: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Performs full matching analysis between a resume and target job description.
        """
        # 1. Extract skills from both documents
        resume_skills_data = skill_extractor.extract_skills(resume_text, sections_dict)
        jd_skills_data = skill_extractor.extract_skills(jd_text)

        resume_skill_names = {s["name"] for s in resume_skills_data}
        jd_skill_names = {s["name"] for s in jd_skills_data}

        # 2. Categorize matched vs missing vs bonus skills
        matched_names = resume_skill_names.intersection(jd_skill_names)
        missing_names = jd_skill_names.difference(resume_skill_names)
        extra_names = resume_skill_names.difference(jd_skill_names)

        # Build detailed matched and missing skill lists with categories
        matched_skills = [s for s in resume_skills_data if s["name"] in matched_names]
        missing_skills = [s for s in jd_skills_data if s["name"] in missing_names]
        extra_skills = [s for s in resume_skills_data if s["name"] in extra_names]

        # 3. Calculate metrics
        total_required = len(jd_skill_names)
        skill_coverage_score = round((len(matched_names) / max(1, total_required)) * 100.0, 1) if total_required > 0 else 100.0

        # 4. Text Cosine Similarity
        text_similarity_score = self.calculate_text_similarity(resume_text, jd_text)

        # 5. Composite Match Score
        # If JD specified skills, weigh both skill coverage (55%) and general text similarity (45%)
        if total_required > 0:
            final_match_score = round((0.55 * skill_coverage_score) + (0.45 * text_similarity_score), 1)
        else:
            final_match_score = text_similarity_score

        # Bound to [0, 100]
        final_match_score = max(0.0, min(100.0, final_match_score))

        # 6. Generate explainability insights
        evidence_points = []
        for s in matched_skills:
            if s.get("sections"):
                evidence_points.append(f"{s['name']} verified in {', '.join(s['sections']).title()} section(s)")
            else:
                evidence_points.append(f"{s['name']} mentioned {s['frequency']} time(s) in resume")

        return {
            "overall_match_score": final_match_score,
            "skill_coverage_score": skill_coverage_score,
            "text_similarity_score": text_similarity_score,
            "total_jd_skills": total_required,
            "matched_skills_count": len(matched_names),
            "missing_skills_count": len(missing_names),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills,
            "evidence_points": evidence_points[:8]
        }

# Global singleton instance
job_matcher = JobMatcher()
