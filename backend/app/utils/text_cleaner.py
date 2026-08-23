"""
Text cleaning and normalization utility functions for Resume & Job Description processing.
"""

import re
import string
from typing import List

# Common English stopwords (comprehensive list without needing external NLTK download)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

def clean_raw_text(text: str) -> str:
    """
    Cleans raw resume or job description text by removing URLs, emails, phone numbers,
    control characters, and excessive whitespace while preserving technical keywords.
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' ', text)
    
    # Remove phone numbers (various international formats)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', ' ', text)

    # Normalize special dashes and bullet points to standard space/bullet
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219\u00B7\u25AA\u25CF]', ' ', text)
    text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015]', '-', text)
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201C\u201D]', '"', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_for_nlp(text: str, remove_stopwords: bool = True) -> str:
    """
    Prepares text for TF-IDF vectorization and role classification:
    lowercasing, punctuation handling (preserving C++, C#, .NET), and stopword filtering.
    """
    cleaned = clean_raw_text(text).lower()
    
    # Preserve key symbols in technical terms: c++, c#, .net
    cleaned = re.sub(r'\bc\+\+', 'cpp_token', cleaned)
    cleaned = re.sub(r'\bc#', 'csharp_token', cleaned)
    cleaned = re.sub(r'\.net\b', 'dotnet_token', cleaned)
    
    # Remove remaining punctuation except underscores
    tokens = re.findall(r'\b[a-zA-Z0-9_+#.-]+\b', cleaned)
    
    processed_tokens = []
    for token in tokens:
        clean_tok = token.strip(string.punctuation)
        if not clean_tok:
            continue

        # Restore special tokens
        if clean_tok == 'cpp_token':
            clean_tok = 'c++'
        elif clean_tok == 'csharp_token':
            clean_tok = 'c#'
        elif clean_tok == 'dotnet_token':
            clean_tok = '.net'

        if remove_stopwords and clean_tok in STOPWORDS:
            continue

        if len(clean_tok) > 1 or clean_tok in {'c', 'r'}:
            processed_tokens.append(clean_tok)
            
    return " ".join(processed_tokens)
