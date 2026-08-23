"""
End-to-End Training & Model Comparison Pipeline for Resume Role Classification.
Ensures zero data leakage by fitting TF-IDF only on training fold.
Benchmarks Logistic Regression, Calibrated LinearSVC, Multinomial Naive Bayes, and Random Forest.
"""

import json
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

from backend.app.ml.preprocess import preprocess_text_series
from backend.app.ml.evaluate import evaluate_classifier

def train_and_evaluate_models(data_path: str = "backend/data/raw/resume_role_dataset.csv", output_dir: str = "backend/app/models"):
    print("=" * 60)
    print("Starting SkillMatch ML Role Classifier Training Pipeline")
    print("=" * 60)
    
    # 1. Load dataset
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples from {data_path}")
    print(f"Class distribution:\n{df['role'].value_counts()}\n")
    
    # 2. Preprocess text
    print("Normalizing and cleaning text documents...")
    df['cleaned_text'] = preprocess_text_series(df['resume_text'])
    
    # 3. Encode labels
    label_encoder = LabelEncoder()
    df['label'] = label_encoder.fit_transform(df['role'])
    class_names = list(label_encoder.classes_)
    print(f"Target classes ({len(class_names)}): {class_names}\n")
    
    # 4. Stratified Train / Test split (80% Train, 20% Test)
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        df['cleaned_text'],
        df['label'],
        test_size=0.20,
        random_state=42,
        stratify=df['label']
    )
    print(f"Train split: {len(X_train_raw)} samples | Test split: {len(X_test_raw)} samples")
    
    # 5. Fit TF-IDF strictly on training set (No Data Leakage)
    print("Fitting TF-IDF Vectorizer on training set...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=2500,
        sublinear_tf=True,
        min_df=2
    )
    X_train_tfidf = vectorizer.fit_transform(X_train_raw)
    X_test_tfidf = vectorizer.transform(X_test_raw)
    print(f"Extracted {X_train_tfidf.shape[1]} TF-IDF feature tokens.\n")
    
    # 6. Define candidate models
    candidate_models = {
        "Logistic Regression": LogisticRegression(
            C=2.0,
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        ),
        "Calibrated LinearSVC": CalibratedClassifierCV(
            estimator=LinearSVC(class_weight='balanced', random_state=42, dual=True),
            cv=3
        ),
        "Multinomial Naive Bayes": MultinomialNB(
            alpha=0.1
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=20,
            random_state=42
        )
    }
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None
    
    print("-" * 60)
    print(f"{'Model':<25} | {'Accuracy':<10} | {'F1 (Macro)':<12} | {'F1 (Weighted)':<12}")
    print("-" * 60)
    
    for name, model in candidate_models.items():
        # Train
        model.fit(X_train_tfidf, y_train)
        
        # Predict on Test
        y_pred = model.predict(X_test_tfidf)
        
        # Evaluate
        eval_metrics = evaluate_classifier(y_test.values, y_pred, class_names)
        results[name] = eval_metrics
        
        acc = eval_metrics["accuracy"]
        f1_m = eval_metrics["f1_macro"]
        f1_w = eval_metrics["f1_weighted"]
        
        print(f"{name:<25} | {acc:<10.4f} | {f1_m:<12.4f} | {f1_w:<12.4f}")
        
        if f1_m > best_f1:
            best_f1 = f1_m
            best_model_name = name
            best_model_obj = model
            
    print("-" * 60)
    print(f"\nBest Model Selected: {best_model_name} (Macro F1 = {best_f1:.4f})\n")
    
    # 7. Serialize Artifacts
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(best_model_obj, out_path / "role_classifier.pkl")
    joblib.dump(vectorizer, out_path / "tfidf_vectorizer.pkl")
    joblib.dump(label_encoder, out_path / "label_encoder.pkl")
    
    # Save overall evaluation report JSON
    report_data = {
        "best_model": best_model_name,
        "best_macro_f1": best_f1,
        "classes": class_names,
        "model_comparisons": results
    }
    
    with open(out_path / "evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    print(f"Artifacts successfully saved to {out_path.resolve()}:")
    print(f"  - role_classifier.pkl")
    print(f"  - tfidf_vectorizer.pkl")
    print(f"  - label_encoder.pkl")
    print(f"  - evaluation_report.json")
    print("=" * 60)
    
    return report_data

if __name__ == "__main__":
    train_and_evaluate_models()
