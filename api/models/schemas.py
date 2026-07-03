from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Verdict(str, Enum):
    VALIDE = "VALIDE"
    DOUTEUSE = "DOUTEUSE"
    ILLISIBLE = "ILLISIBLE"


class PlaquResult(BaseModel):
    texte: str
    texte_brut: str
    bbox: List[int]
    score_detection: float
    conf_ocr: float
    valide: bool
    verdict: Verdict
    moteur_ocr: Optional[str] = None


class DetectResponse(BaseModel):
    plaques: List[PlaquResult]
    nb_plaques: int
    temps_ms: float
    erreur: Optional[str] = None