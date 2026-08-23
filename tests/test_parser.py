"""
Unit tests for Resume Parser and Section Detector.
"""

import unittest
from backend.app.services.resume_parser import resume_parser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.sample_text = """
Jane Doe | jane.doe@gmail.com | +1 555-987-6543 | github.com/janedoe | linkedin.com/in/janedoe

SUMMARY:
Software developer with 1 year of experience in Python and web development.

TECHNICAL SKILLS:
Python, JavaScript, React, FastAPI, SQL, Git, Docker

PROJECTS:
- Real-time chat application with WebSocket and FastAPI.
- Portfolio website using React and Tailwind CSS.

EXPERIENCE:
Software Engineering Intern at Tech Corp (2023 - 2024).

EDUCATION:
Bachelor of Science in Computer Science, State University.
"""

    def test_parse_sections(self):
        result = resume_parser.parse(self.sample_text)
        sections = result["sections"]
        
        self.assertIn("summary", sections)
        self.assertIn("skills", sections)
        self.assertIn("projects", sections)
        self.assertIn("experience", sections)
        self.assertIn("education", sections)

    def test_contact_info_extraction(self):
        result = resume_parser.parse(self.sample_text)
        contact = result["contact_info"]
        
        self.assertEqual(contact["email"], "jane.doe@gmail.com")
        self.assertIn("555-987-6543", contact["phone"])
        self.assertIsNotNone(contact["github"])
        self.assertIsNotNone(contact["linkedin"])

if __name__ == "__main__":
    unittest.main()
