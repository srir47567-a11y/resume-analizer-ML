"""
Unit tests for Machine Learning Role Classifier & Preprocessing.
"""

import unittest
from backend.app.ml.preprocess import normalize_for_nlp
from backend.app.ml.predict import role_classifier_service

class TestMLClassification(unittest.TestCase):
    def test_text_normalization(self):
        raw = "Proficient in Python3, C++, C#, .NET and Scikit-Learn! Contact: test@mail.com"
        norm = normalize_for_nlp(raw)
        self.assertIn("python3", norm)
        self.assertIn("c++", norm)
        self.assertIn("c#", norm)
        self.assertIn(".net", norm)
        self.assertNotIn("test@mail.com", norm)

    def test_role_prediction_data_analyst(self):
        text = "Experienced in SQL queries, Power BI reports, Tableau dashboards, Excel spreadsheets, and Pandas exploratory data analysis."
        result = role_classifier_service.predict_roles(text)
        
        self.assertEqual(result["top_role"], "Data Analyst")
        self.assertGreater(result["top_confidence"], 30.0)
        self.assertIsInstance(result["predictions"], list)
        self.assertGreater(len(result["predictions"]), 0)

    def test_role_prediction_frontend(self):
        text = "Frontend specialist skilled in React, TypeScript, Tailwind CSS, Next.js, Redux state management, and responsive web design."
        result = role_classifier_service.predict_roles(text)
        
        self.assertEqual(result["top_role"], "Frontend Developer")
        self.assertGreater(result["top_confidence"], 30.0)

if __name__ == "__main__":
    unittest.main()
