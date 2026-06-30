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
        self.langues = langues or ["fr"]
        self._reader = easyocr.Reader(self.langues, gpu=False)

    def lire(self, crop) -> OcrResult:
        resultats = self._reader.readtext(crop)
        if not resultats:
            return OcrResult(texteBrut="", confOcr=0.0)
        _, texte, confiance = max(resultats, key=lambda r: r[2])
        return OcrResult(texteBrut=texte, confOcr=float(confiance))


class TesseractEngine(OcrEngine):
    def __init__(self, config="--psm 7"):
        self.config = config

    def lire(self, crop) -> OcrResult:
        texte = pytesseract.image_to_string(crop, config=self.config).strip()
        data = pytesseract.image_to_data(crop, config=self.config, output_type=pytesseract.Output.DICT)
        confiances = [int(c) for c in data["conf"] if c not in ("-1",) and int(c) >= 0]
        confiance_moy = (sum(confiances) / len(confiances) / 100) if confiances else 0.0
        return OcrResult(texteBrut=texte, confOcr=confiance_moy)
