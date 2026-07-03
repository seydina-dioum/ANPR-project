"""
Initialisation du service ANPR avec les vraies classes OCR et détection.
Ce fichier est le point de jonction entre l'API (camarade télécom)
et les modules OCR (Adji) + détection (Membre A).
"""
from detection.detector import DetecteurYOLO
from ocr.preprocessor import Preprocesseur
from ocr.ocr_engine import EasyOcrEngine
from ocr.validator import Validateur
from api.services.pipeline import AnprService

def creer_service(modele_path: str = "detection/models/anpr_best.pt") -> AnprService:
    detecteur = DetecteurYOLO(modele_path=modele_path)
    detecteur.charger_modele()

    preproc = Preprocesseur()
    ocr = EasyOcrEngine()
    validateur = Validateur()

    return AnprService(
        detecteur=detecteur,
        preproc=preproc,
        ocr=ocr,
        validateur=validateur,
    )

# Instance globale utilisée par l'API
service = creer_service()
