"""
Preprocessing pipeline module for ML model inputs.
"""

from typing import List, Union
import pandas as pd
from backend.app.utils.text_cleaner import normalize_for_nlp

def preprocess_text_series(texts: Union[List[str], pd.Series]) -> List[str]:
    """
    Preprocess a collection of raw text documents for TF-IDF training or inference.
    """
    return [normalize_for_nlp(str(t)) for t in texts]

def preprocess_single_document(text: str) -> str:
    """
    Preprocess a single document (e.g. uploaded resume or pasted job description).
    """
    return normalize_for_nlp(text)
