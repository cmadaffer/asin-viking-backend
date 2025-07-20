from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, allow all. Later you can lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ASINCheckRequest(BaseModel):
    asins: List[str]
    marketplace_id: str

class ASINCheckResult(BaseModel):
    asin: str
    status: str
    restriction_type: Optional[str]
    approval_required: bool

class ASINCheckResponse(BaseModel):
    results: List[ASINCheckResult]

mock_asin_data = {
    "B089KV4YYX": {"status": "gated", "restriction_type": "brand", "approval_required": True},
    "B07PGL2ZSL": {"status": "open", "restriction_type": None, "approval_required": False},
    "B08CFSZLQ4": {"status": "restricted", "restriction_type": "hazmat", "approval_required": True},
}

@app.post("/check-asins", response_model=ASINCheckResponse)
def check_asins(request: ASINCheckRequest):
    results = []
    for asin in request.asins:
        data = mock_asin_data.get(asin, {"status": "unknown", "restriction_type": None, "approval_required": False})
        result = ASINCheckResult(
            asin=asin,
            status=data["status"],
            restriction_type=data["restriction_type"],
            approval_required=data["approval_required"]
        )
        results.append(result)
    return ASINCheckResponse(results=results)

@app.get("/")
def read_root():
    return {"message": "ASIN Viking API is live. Use /check-asins to check gating."}

