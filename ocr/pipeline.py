import cv2
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ultralytics import YOLO
from ocr.preprocessor import Preprocesseur
from ocr.ocr_engine import EasyOcrEngine, TesseractEngine
from ocr.validator import Validateur, Verdict


class PipelineANPR:

    def __init__(self, modele_path="yolov8n.pt", moteur="easyocr"):
        self.detecteur = YOLO(modele_path)
        self.preproc = Preprocesseur()
        self.validateur = Validateur()

        if moteur == "tesseract":
            self.ocr = TesseractEngine()
        else:
            self.ocr = EasyOcrEngine()

    def analyser(self, image_path: str) -> dict:
        import time
        t0 = time.time()

        image = cv2.imread(image_path)
        if image is None:
            return {"erreur": "Image illisible", "plaques": [], "nb_plaques": 0, "temps_ms": 0}

        resultats = self.detecteur(image, verbose=False)
        plaques = []

        for r in resultats:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                score_detection = round(float(box.conf), 4)

                crop = image[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                crop_pretraite = self.preproc.pretraiter(crop)
                ocr_result = self.ocr.lire(crop_pretraite)
                verdict = self.validateur.valider(ocr_result.texteBrut)

                plaques.append({
                    "texte": self.validateur.normaliser(ocr_result.texteBrut),
                    "texte_brut": ocr_result.texteBrut,
                    "bbox": [x1, y1, x2, y2],
                    "score_detection": score_detection,
                    "conf_ocr": round(ocr_result.confOcr, 4),
                    "valide": verdict == Verdict.VALIDE,
                    "verdict": verdict.value
                })

        temps_ms = int((time.time() - t0) * 1000)
        return {
            "plaques": plaques,
            "nb_plaques": len(plaques),
            "temps_ms": temps_ms
        }


if __name__ == "__main__":
    pipeline = PipelineANPR(modele_path="yolov8n.pt", moteur="easyocr")

    images = [
        "ocr/test_crops/plaque1.jpg",
        "ocr/test_crops/plaque3.jpg",
        "ocr/test_crops/plaque5.jpg",
    ]

    for img in images:
        print(f"\n=== {img} ===")
        resultat = pipeline.analyser(img)
        print(f"Plaques detectees : {resultat['nb_plaques']}")
        print(f"Temps : {resultat['temps_ms']} ms")
        for p in resultat["plaques"]:
            print(f"  texte='{p['texte']}'  conf_ocr={p['conf_ocr']}  verdict={p['verdict']}")
        if resultat['nb_plaques'] == 0:
            print("  (aucune plaque detectee par YOLOv8 generique sur cette image)")
