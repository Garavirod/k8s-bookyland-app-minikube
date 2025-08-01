from fastapi import APIRouter, HTTPException
from environment import FAIL_LIVENESS, FAIL_READINESS
import random
router = APIRouter(prefix='/health')

fail_liveness = FAIL_LIVENESS == 'true'
fail_readiness = random.random() < 0.5 if FAIL_READINESS == 'true' else False

print(f"Fail liveness: {fail_liveness}")    
print(f"Fail readiness: {fail_readiness}")

# Readiness and liveness endpoints
@router.get("/ready")
async def readiness_check():
    if fail_readiness:
        raise HTTPException(status_code=503, detail="Service is not ready")
    return {"status": "ready", "message": "Service is ready"}

@router.get("/up")
async def readiness_check():
    return {"status": "Up", "message": "Service is Up"}

@router.get("/health")
async def liveness_check():
    if fail_liveness:
        raise HTTPException(status_code=503, detail="Service is not healthy")
    return {"status": "healthy", "message": "Service is healthy"}
