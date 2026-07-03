from typing import List
from api.models.schemas import PlaquResult, Verdict
from api.utils.image import bytes_to_cv2


class AnprService:
    def __init__(self, detecteur=None, preproc=None, ocr=None, validateur=None):
        self.detecteur = detecteur
        self.preproc = preproc
        self.ocr = ocr
        self.validateur = validateur

    async def analyser(self, image_bytes: bytes) -> List[PlaquResult]:
        image = bytes_to_cv2(image_bytes)

        if self.detecteur is None or self.ocr is None:
            return []

        detections = self.detecteur.traiter(image)
        resultats = []

        for det in detections:
            crop = det["crop"]
            bbox_dict = det["bbox"]

            bbox_liste = [
                bbox_dict["x1"],
                bbox_dict["y1"],
                bbox_dict["x2"],
                bbox_dict["y2"]
            ]
            score = bbox_dict["confiance"]

            if bbox_dict.get("classe") == "Invalid plate":
                continue

            crop_propre = self.preproc.pretraiter(crop)
            ocr_result = self.ocr.lire(crop_propre)
            verdict_enum = self.validateur.valider(ocr_result.texteBrut)
            texte = self.validateur.normaliser(ocr_result.texteBrut)

            resultats.append(PlaquResult(
                texte=texte,
                texte_brut=ocr_result.texteBrut,
                bbox=bbox_liste,
                score_detection=score,
                conf_ocr=ocr_result.confOcr,
                valide=(verdict_enum.value == "VALIDE"),
                verdict=Verdict(verdict_enum.value),
                moteur_ocr="EasyOCR"
            ))

        return resultats


_service = AnprService()


async def run_pipeline(image_bytes: bytes) -> List[PlaquResult]:
    return await _service.analyser(image_bytes)
