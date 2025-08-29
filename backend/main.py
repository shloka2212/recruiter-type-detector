from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # for AWS Lambda later

from detector import predict_job_type           # <- updated
from retriever import retrieve_evidence, explain_with_template  # <- updated for consulting vs real

app = FastAPI(title="Recruiter Type Detector")

# CORS so the React site can call this API later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # keep * in dev; tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobInput(BaseModel):
    description: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(job: JobInput):
    """
    1) Predict recruiter type: consulting vs real (ML if available, rules fallback)
    2) Retrieve similar patterns (RAG-style evidence)
    3) Generate a friendly explanation (template)
    """
    label = predict_job_type(job.description)                 # "consulting" or "real"
    evidence = retrieve_evidence(job.description, top_k=2)    # short, pattern-based evidence
    explanation = explain_with_template(job.description, label, evidence)

    return {
        "status": label,
        "evidence": evidence,
        "explanation": explanation
    }

# for AWS Lambda
handler = Mangum(app)
