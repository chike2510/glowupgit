from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from agent.agent import run_glowup

app = FastAPI(title="glowupgit API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class GlowupRequest(BaseModel):
    url: HttpUrl

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/glowup")
def glowup(payload: GlowupRequest):
    try:
        return run_glowup(str(payload.url))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not read repository: {exc}") from exc
