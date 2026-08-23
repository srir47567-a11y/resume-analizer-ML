"""
Model inference module for Role Prediction and Explainability.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import joblib
import numpy as np

from backend.app.ml.preprocess import preprocess_single_document

class RoleClassifierService:
    def __init__(self, models_dir: str = "backend/app/models"):
        self.models_dir = Path(models_dir)
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.is_loaded = False
        
    def load_artifacts(self):
        if not self.is_loaded:
            model_path = self.models_dir / "role_classifier.pkl"
            vec_path = self.models_dir / "tfidf_vectorizer.pkl"
            le_path = self.models_dir / "label_encoder.pkl"
            
            if not (model_path.exists() and vec_path.exists() and le_path.exists()):
                raise FileNotFoundError(
                    f"Model artifacts not found in {self.models_dir}. Please run training pipeline first."
                )
                
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vec_path)
            self.label_encoder = joblib.load(le_path)
            self.is_loaded = True

    def predict_roles(self, raw_text: str, top_k: int = 4) -> Dict[str, Any]:
        """
        Predicts top candidate job roles with calibrated probabilities and key contributing tokens.
        """
        self.load_artifacts()
        
        cleaned = preprocess_single_document(raw_text)
        if not cleaned:
            return {
                "top_role": "Unknown",
                "top_confidence": 0.0,
                "predictions": [],
                "influential_keywords": []
            }
            
        # Vectorize
        tfidf_vec = self.vectorizer.transform([cleaned])
        
        # Probabilities
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(tfidf_vec)[0]
        elif hasattr(self.model, "decision_function"):
            decision = self.model.decision_function(tfidf_vec)[0]
            # Softmax
            exp_d = np.exp(decision - np.max(decision))
            probs = exp_d / exp_d.sum()
        else:
            pred_idx = self.model.predict(tfidf_vec)[0]
            probs = np.zeros(len(self.label_encoder.classes_))
            probs[pred_idx] = 1.0
            
        classes = self.label_encoder.classes_
        
        # Sort by highest probability
        sorted_indices = np.argsort(probs)[::-1]
        
        predictions = []
        for idx in sorted_indices[:top_k]:
            prob = float(probs[idx])
            predictions.append({
                "role": str(classes[idx]),
                "probability": round(prob, 4),
                "confidence_percentage": round(prob * 100, 1)
            })
            
        top_prediction = predictions[0] if predictions else {"role": "Unknown", "confidence_percentage": 0.0}
        
        # Extract top influential TF-IDF terms present in this resume
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        row_indices = tfidf_vec.tocoo().col
        row_values = tfidf_vec.tocoo().data
        
        # Sort terms by TF-IDF weight in this specific document
        top_token_indices = np.argsort(row_values)[::-1][:10]
        influential_keywords = [
            {"token": str(feature_names[row_indices[i]]), "weight": round(float(row_values[i]), 3)}
            for i in top_token_indices
        ] if len(row_indices) > 0 else []
        
        return {
            "top_role": top_prediction["role"],
            "top_confidence": top_prediction["confidence_percentage"],
            "predictions": predictions,
            "influential_keywords": influential_keywords
        }

# Global singleton instance
role_classifier_service = RoleClassifierService()
