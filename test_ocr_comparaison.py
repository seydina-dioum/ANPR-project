import cv2
import glob
from ocr.ocr_engine import EasyOcrEngine, TesseractEngine
from ocr.validator import Validateur
from ocr.preprocessor import Preprocesseur

easy = EasyOcrEngine()
tess = TesseractEngine()
validateur = Validateur()
preproc = Preprocesseur()

fichiers = sorted(glob.glob("ocr/test_crops/*.*"))

for chemin in fichiers:
    img = cv2.imread(chemin)

    if img is None:
        print(f"\n=== {chemin} ===")
        print("IMPOSSIBLE A LIRE (format non supporté par OpenCV)")
        continue

    img_pretraitee = preproc.pretraiter(img)

    r_easy = easy.lire(img_pretraitee)
    r_tess = tess.lire(img_pretraitee)

    print(f"\n=== {chemin} (après prétraitement) ===")
    print(f"EasyOCR   : texte='{r_easy.texteBrut}'  conf={r_easy.confOcr:.2f}  verdict={validateur.valider(r_easy.texteBrut).value}")
    print(f"Tesseract : texte='{r_tess.texteBrut}'  conf={r_tess.confOcr:.2f}  verdict={validateur.valider(r_tess.texteBrut).value}")
