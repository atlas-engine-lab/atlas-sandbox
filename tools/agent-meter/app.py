from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI(title="Agent Meter API", version="0.1.0")

class ValidateRequest(BaseModel):
    task: str
    output: str

class ValidateResponse(BaseModel):
    usefulness_score: int
    issues: List[str]
    free_tier_remaining: int
    paid_path: str

@app.get('/health')
def health():
    return {"ok": True, "service": "agent-meter", "version": "0.1.0"}

@app.post('/v1/validate', response_model=ValidateResponse)
def validate(req: ValidateRequest):
    issues = []
    score = 80

    if len(req.output.strip()) < 80:
        issues.append("output_too_short")
        score -= 20

    if re.search(r"\b(lorem ipsum|todo|tbd)\b", req.output.lower()):
        issues.append("placeholder_content")
        score -= 25

    if 'next step' not in req.output.lower() and 'action' not in req.output.lower():
        issues.append("missing_actionability")
        score -= 15

    score = max(0, min(100, score))

    return ValidateResponse(
        usefulness_score=score,
        issues=issues,
        free_tier_remaining=99,
        paid_path="x402/USDC pay-per-request (planned)"
    )
