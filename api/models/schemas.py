from pydantic import BaseModel
from typing import List, Optional

class PlaquResult(BaseModel):
    texte: str
    texte_brut: str
    bbox: List[int]
    score_detection: float
    conf_ocr: float
    valide: bool
    moteur_ocr: Optional[str] = None

class DetectResponse(BaseModel):
    plaques: List[PlaquResult]
    nb_plaques: int
    temps_ms: float
    erreur: Optional[str] = None