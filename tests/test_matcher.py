"""
Unit tests for Skill Extractor, Job Matcher, and Roadmap Generator.
"""

import unittest
from backend.app.services.skill_extractor import skill_extractor
from backend.app.services.matcher import job_matcher
from backend.app.services.roadmap import roadmap_generator

class TestMatcherAndRoadmap(unittest.TestCase):
    def test_skill_extraction_and_alias_normalization(self):
        text = "Skilled in python3, sklearn, power bi, postgresql, and reactjs."
        skills = skill_extractor.extract_skills(text)
        skill_names = [s["name"] for s in skills]
        
        self.assertIn("Python", skill_names)
        self.assertIn("Scikit-learn", skill_names)
        self.assertIn("Power BI", skill_names)
        self.assertIn("PostgreSQL", skill_names)
        self.assertIn("React", skill_names)

    def test_job_matching_calculation(self):
        resume = "Python, FastAPI, SQL, PostgreSQL, Git, Linux"
        jd = "Looking for Python backend developer with FastAPI, PostgreSQL, Docker, AWS, and Git."
        
        match = job_matcher.match(resume, jd)
        self.assertGreater(match["overall_match_score"], 0.0)
        self.assertLessEqual(match["overall_match_score"], 100.0)
        
        matched_names = [s["name"] for s in match["matched_skills"]]
        missing_names = [s["name"] for s in match["missing_skills"]]
        
        self.assertIn("Python", matched_names)
        self.assertIn("FastAPI", matched_names)
        self.assertIn("Docker", missing_names)
        self.assertIn("AWS", missing_names)

    def test_roadmap_generation(self):
        current_skills = ["Python", "FastAPI"]
        missing_skills = [
            {"name": "Docker", "category": "DevOps & Cloud"},
            {"name": "AWS", "category": "DevOps & Cloud"},
            {"name": "PostgreSQL", "category": "Databases"}
        ]
        
        roadmap = roadmap_generator.generate_roadmap(
            current_skills=current_skills,
            missing_skills=missing_skills,
            target_role="Backend Developer",
            overall_match_score=60.0
        )
        
        self.assertGreater(len(roadmap["roadmap_steps"]), 2)
        self.assertEqual(roadmap["total_gaps"], 3)
        self.assertIn("prioritized_skills", roadmap)

if __name__ == "__main__":
    unittest.main()
