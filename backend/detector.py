# detector.py
import re
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "baseline_model.pkl"
VECTORIZER_PATH = Path(__file__).parent / "vectorizer.pkl"

try:
    clf = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    USE_ML = True
    print("Recruiter-type ML baseline loaded successfully.")
except FileNotFoundError:
    print("ML model not found. Falling back to keyword rules.")
    USE_ML = False

# Strong consulting signals
CONSULTING_TERMS = [
    # visas / work auth
    "h1b", "opt", "stem opt", "cpt", "h4 ead", "l2 ead", "gc", "gc transfer",
    "visa sponsorship", "sponsorship",
    # staffing language
    "vendors", "vendor", "clients", "client sites", "implementation partner",
    "implementation partners", "third-party", "third party", "c2c", "corp to corp", "w2 only",
    "bench", "bench sales", "marketing", "placement", "relocation",
    # social-call-to-action patterns
    "comment \"interested\"", "comment “interested”", "comment interested",
    "drop \"interested\"", "dm me your resume", "dm your resume", "whatsapp",
    # signals often seen in blasts
    "multiple openings", "nationwide", "fresh grads encouraged", "quick placements",
    "training", "on the job support", "e-verified", "stemon opt",  # common misspellings too
]

def consulting_signal_score(text: str) -> int:
    t = text.lower()
    hits = 0
    for term in CONSULTING_TERMS:
        if term in t:
            hits += 1
    # Count heavy hashtag usage as a weak signal
    hashtags = t.count("#")
    if hashtags >= 5:
        hits += 1
    return hits

def predict_job_type(description: str) -> str:
    """
    Returns "consulting" or "real".
    Uses ML + a small rule-based override for strong consulting signals.
    """
    text = description.strip()

    if USE_ML:
        X_vec = vectorizer.transform([text])
        pred = clf.predict(X_vec)[0]  # "consulting" or "real"

        # If we can get probabilities, use them to decide when to trust rules
        proba = None
        try:
            proba = clf.predict_proba(X_vec)[0]
            # Map class -> prob
            classes = list(clf.classes_)
            p_cons = proba[classes.index("consulting")] if "consulting" in classes else None
            p_real = proba[classes.index("real")] if "real" in classes else None
        except Exception:
            p_cons = p_real = None

        # Compute signals
        sig = consulting_signal_score(text)

        # Override logic:
        # If model says "real" but we see >=2 strong consulting signals,
        # OR model confidence is low (<0.65) and there is at least 1 signal -> flip to consulting.
        if pred == "real":
            if sig >= 2:
                return "consulting"
            if p_real is not None and p_real < 0.65 and sig >= 1:
                return "consulting"
        return pred

    # Fallback: pure rules
    sig = consulting_signal_score(text)
    if sig >= 2:
        return "consulting"
    return "real"
