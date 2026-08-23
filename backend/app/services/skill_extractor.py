"""
Skill Extractor and Normalizer Service.
Matches skills and aliases from text using compiled boundary regex patterns.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple

class SkillExtractor:
    def __init__(self, skills_json_path: str = "backend/data/skills.json"):
        self.skills_json_path = Path(skills_json_path)
        self.skills_db: List[Dict[str, Any]] = []
        self.canonical_map: Dict[str, Dict[str, Any]] = {} # alias_lower -> canonical info
        self.compiled_patterns: List[Tuple[re.Pattern, str]] = []
        self.is_loaded = False
        self._load_skills()

    def _load_skills(self):
        if not self.skills_json_path.exists():
            raise FileNotFoundError(f"Skills database not found at {self.skills_json_path}")

        with open(self.skills_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.skills_db = data.get("skills", [])

        self.canonical_map = {}
        patterns = []

        # Sort aliases by length descending so longer phrases match first (e.g. 'Power BI' before 'Power')
        all_aliases = []
        for skill_info in self.skills_db:
            canonical_name = skill_info["name"]
            category = skill_info.get("category", "General")
            aliases = skill_info.get("aliases", [canonical_name])

            # Ensure canonical name is in aliases
            if canonical_name.lower() not in [a.lower() for a in aliases]:
                aliases.append(canonical_name)

            for alias in aliases:
                alias_lower = alias.lower()
                self.canonical_map[alias_lower] = {
                    "name": canonical_name,
                    "category": category
                }
                all_aliases.append((alias_lower, canonical_name))

        # Sort by length descending
        all_aliases.sort(key=lambda x: len(x[0]), reverse=True)

        for alias_lower, canonical_name in all_aliases:
            # Escape regex special characters, handle + and #
            escaped = re.escape(alias_lower)
            # Create regex with word boundary or start/end of string
            # Handle special cases like C++, C#, .NET where word boundary \b doesn't work after + or #
            if alias_lower.endswith('+') or alias_lower.endswith('#'):
                pattern_str = r'(?<![a-zA-Z0-9])' + escaped + r'(?![a-zA-Z0-9])'
            elif alias_lower.startswith('.'):
                pattern_str = r'(?<![a-zA-Z0-9])' + escaped + r'\b'
            else:
                pattern_str = r'\b' + escaped + r'\b'

            compiled_p = re.compile(pattern_str, re.IGNORECASE)
            patterns.append((compiled_p, alias_lower))

        self.compiled_patterns = patterns
        self.is_loaded = True

    def extract_skills(self, text: str, sections_dict: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Extracts all canonical skills from text, deduplicating and attributing section context.
        """
        if not text:
            return []

        if not self.is_loaded:
            self._load_skills()

        detected_skills: Dict[str, Dict[str, Any]] = {}
        text_lower = text.lower()

        # Track which sections contain each skill if sections provided
        for pattern, alias_lower in self.compiled_patterns:
            matches = list(pattern.finditer(text_lower))
            if matches:
                info = self.canonical_map[alias_lower]
                canonical_name = info["name"]
                category = info["category"]

                if canonical_name not in detected_skills:
                    detected_skills[canonical_name] = {
                        "name": canonical_name,
                        "category": category,
                        "frequency": len(matches),
                        "matched_aliases": [alias_lower],
                        "sections": []
                    }
                else:
                    detected_skills[canonical_name]["frequency"] += len(matches)
                    if alias_lower not in detected_skills[canonical_name]["matched_aliases"]:
                        detected_skills[canonical_name]["matched_aliases"].append(alias_lower)

        # Attribute sections
        if sections_dict:
            for sec_name, sec_text in sections_dict.items():
                sec_lower = sec_text.lower()
                for canonical_name, skill_data in detected_skills.items():
                    for alias in skill_data["matched_aliases"]:
                        if alias in sec_lower:
                            if sec_name not in skill_data["sections"]:
                                skill_data["sections"].append(sec_name)
                            break

        # Convert to sorted list by frequency and category
        result = list(detected_skills.values())
        result.sort(key=lambda x: (-x["frequency"], x["name"]))
        return result

    def get_skill_names_set(self, text: str) -> Set[str]:
        """Returns just a set of canonical skill names found in text."""
        extracted = self.extract_skills(text)
        return {item["name"] for item in extracted}

# Global singleton instance
skill_extractor = SkillExtractor()
