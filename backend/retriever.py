from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Patterns that distinguish consulting recruiters vs real recruiters.
# Keep these short and readable—returned to the UI as "evidence".
PATTERNS = [
    # Consulting indicators
    "Mentions H1B, OPT, or CPT sponsorship frequently.",
    "Emphasizes training, placement programs, or bench marketing.",
    "Refers to third-party clients or implementation partners.",
    "Requests contact via WhatsApp or generic email instead of company portal.",
    "Uses generic role descriptions without a company name or product.",
    "Focuses on relocation to client sites or nationwide project deployment.",
    # Real recruiter indicators
    "Includes company or product name and describes the team or mission.",
    "Uses official application links (company careers page or LinkedIn post).",
    "Avoids visa/bench/training language and focuses on the role’s responsibilities.",
    "Tone is authentic and specific rather than mass-blast with emojis/hashtags.",
]

# Load a small embedding model (downloads once on first run)
_model = SentenceTransformer("all-MiniLM-L6-v2")
_PATTERN_EMB = _model.encode(PATTERNS, convert_to_numpy=True)

def _embed(texts: List[str]) -> np.ndarray:
    return _model.encode(texts, convert_to_numpy=True)

def retrieve_evidence(user_text: str, top_k: int = 2) -> List[str]:
    """
    Ranks pattern statements by similarity to the user's text and returns top_k as lightweight evidence.
    """
    q_emb = _embed([user_text])  # shape (1, dim)
    sims = cosine_similarity(q_emb, _PATTERN_EMB)[0]  # shape (n_patterns,)
    top_idx = sims.argsort()[::-1][:top_k]
    return [PATTERNS[i] for i in top_idx]

def explain_with_template(description: str, label: str, evidence: List[str]) -> str:
    """
    Friendly explanation tailored to recruiter type.
    """
    if label == "consulting":
        return (
            "This post appears to be from a consulting or staffing recruiter based on its language. "
            "Notable signals:\n"
            f"- {evidence[0]}\n"
            f"- {evidence[1] if len(evidence) > 1 else ''}\n\n"
            "Consulting recruiters can be legit, but expectations differ from direct-hire roles. "
            "Verify the company relationship (end-client vs. vendor), confirm pay structure (W2/C2C), "
            "and look for an official client/job requisition before proceeding."
        ).strip()
    else:
        return (
            "This post looks like it’s from a direct employer or an in-house recruiter. "
            "Even so, review details on the official careers page and ensure the application flow "
            "uses company domains and verified links."
        )
