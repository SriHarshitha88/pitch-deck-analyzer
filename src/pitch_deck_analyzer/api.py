from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
from .crew import PitchDeckCrew

app = FastAPI(
    title="Pitch Deck Analyzer API",
    description="AI-Driven Pitch Deck Analysis Platform API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crew = PitchDeckCrew()

class AnalysisRequest(BaseModel):
    company_name: str
    website_url: Optional[str] = None

@app.post("/analyze")
async def analyze_pitch_deck(
    file: UploadFile = File(...),
    company_name: str = None,
    website_url: Optional[str] = None
):
    """Analyze a pitch deck and return the results."""
    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        
        result = crew.analyze_pitch_deck(
            pitch_deck_path=file_path,
            company_name=company_name,
            website_url=website_url
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 