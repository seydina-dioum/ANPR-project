import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.models.schemas import DetectResponse

router = APIRouter()

@router.post("/detect", response_model=DetectResponse)
async def detect_plates(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=415,
            detail=f"Format non supporté : {file.content_type}."
        )

    start = time.time()
    image_bytes = await file.read()

    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Fichier image vide.")

    temps_ms = round((time.time() - start) * 1000, 1)

    return DetectResponse(
        plaques=[],
        nb_plaques=0,
        temps_ms=temps_ms,
    )