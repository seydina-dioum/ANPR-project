from abc import ABC, abstractmethod
from dataclasses import dataclass
import pytesseract
import easyocr

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@dataclass
class OcrResult:
    texteBrut: str
    confOcr: float


class OcrEngine(ABC):
    @abstractmethod
    def lire(self, crop) -> OcrResult:
        ...


class EasyOcrEngine(OcrEngine):
    def __init__(self, langues=None):
        # Utiliser "en" au lieu de "fr" : les plaques n'ont pas de caractères accentués
        self.langues = langues or ["en"]
        self._reader = easyocr.Reader(self.langues, gpu=False)
        # Allowlist : uniquement les caractères présents sur les plaques d'immatriculation
        self._allowlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def lire(self, crop) -> OcrResult:
        resultats = self._reader.readtext(
            crop,
            allowlist=self._allowlist,
            detail=1,
            paragraph=False,
        )
        if not resultats:
            return OcrResult(texteBrut="", confOcr=0.0)

        # Trier les segments de gauche à droite par la coordonnée X minimale
        resultats.sort(key=lambda r: min(pt[0] for pt in r[0]))

        # Concaténer TOUS les segments détectés au lieu de ne garder que le meilleur
        textes = []
        confiances = []
        for bbox, texte, confiance in resultats:
            textes.append(texte)
            confiances.append(confiance)

        texte_complet = "".join(textes)
        confiance_moyenne = sum(confiances) / len(confiances) if confiances else 0.0

        return OcrResult(texteBrut=texte_complet, confOcr=float(confiance_moyenne))


class TesseractEngine(OcrEngine):
    def __init__(self, config="--psm 7"):
        self.config = config

    def lire(self, crop) -> OcrResult:
        texte = pytesseract.image_to_string(crop, config=self.config).strip()
        data = pytesseract.image_to_data(crop, config=self.config, output_type=pytesseract.Output.DICT)
        confiances = [int(c) for c in data["conf"] if c not in ("-1",) and int(c) >= 0]
        confiance_moy = (sum(confiances) / len(confiances) / 100) if confiances else 0.0
        return OcrResult(texteBrut=texte, confOcr=confiance_moy)
