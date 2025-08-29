# train_baseline.py
from pathlib import Path
import re
import pandas as pd  # type: ignore
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
import joblib
import numpy as np

# ---------- Paths ----------
ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "job_posts_dataset_expanded.csv"   # <--- place your CSV here
MODEL_PATH = ROOT / "baseline_model.pkl"
VECTORIZER_PATH = ROOT / "vectorizer.pkl"

# ---------- Basic cleaner (keeps semantics, removes noise) ----------
LINK_RE = re.compile(r"https?://\S+")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+")
PHONE_RE = re.compile(r"\+?\d[\d\-\s()]{7,}\d")

def clean_text(s: str) -> str:
    s = s.lower()
    s = LINK_RE.sub(" <link> ", s)
    s = EMAIL_RE.sub(" <email> ", s)
    s = PHONE_RE.sub(" <phone> ", s)
    # normalize some common tokens
    s = s.replace("whatsapp", " whats_app ")
    s = s.replace("c2c", " corp to corp ")
    return s

# ---------- 1. Load dataset ----------
df = pd.read_csv(DATA_PATH)
if not {"description", "label"}.issubset(df.columns):
    raise ValueError("CSV must have columns: 'description', 'label' (labels: 'consulting' or 'real')")

print("Dataset loaded:", df.shape)
df["description"] = df["description"].astype(str).apply(clean_text)
df["label"] = df["label"].astype(str)

# ---------- 2. Train/test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    df["description"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# ---------- 3. Vectorizer ----------
vectorizer = TfidfVectorizer(
    max_features=12000,
    ngram_range=(1, 3),                 # catch "comment interested", "visa sponsorship"
    min_df=2,
    token_pattern=r'(?u)\b[#@]?\w+\b'   # keep #hashtags and words like h1b, c2c
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

# ---------- 4. Class weights (help if data is imbalanced) ----------
classes = np.array(sorted(y_train.unique()))
weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train)


# ---------- 5. Train classifier ----------
clf = LogisticRegression(
    max_iter=1000,
    class_weight={cls: w for cls, w in zip(classes, weights)} 
)
clf.fit(X_train_vec, y_train)

# ---------- 6. Evaluate ----------
y_pred = clf.predict(X_test_vec)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, digits=4))

# ---------- 7. Save artifacts ----------
joblib.dump(clf, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)
print(f"\nSaved model to {MODEL_PATH}")
print(f"Saved vectorizer to {VECTORIZER_PATH}")
