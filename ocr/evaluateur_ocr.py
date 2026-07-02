"""
Evaluateur OCR - Jalon 4
Compare EasyOCR vs Tesseract sur un jeu de test annoté
"""
import cv2
import json
from ocr.preprocessor import Preprocesseur
from ocr.ocr_engine import EasyOcrEngine, TesseractEngine
from ocr.validator import Validateur


def levenshtein(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    ligne_precedente = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        ligne_courante = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = ligne_precedente[j + 1] + 1
            suppressions = ligne_courante[j] + 1
            substitutions = ligne_precedente[j] + (c1 != c2)
            ligne_courante.append(min(insertions, suppressions, substitutions))
        ligne_precedente = ligne_courante
    return ligne_precedente[-1]


def taux_par_caractere(predit: str, verite: str) -> float:
    if len(verite) == 0:
        return 1.0 if len(predit) == 0 else 0.0
    distance = levenshtein(predit.upper(), verite.upper())
    return max(0.0, 1.0 - distance / len(verite))


def evaluer(jeu_de_test: list) -> dict:
    preproc = Preprocesseur()
    easy = EasyOcrEngine()
    tess = TesseractEngine()
    validateur = Validateur()

    resultats = []
    easy_exact = 0
    tess_exact = 0
    easy_car_total = 0.0
    tess_car_total = 0.0

    for item in jeu_de_test:
        chemin = item["image"]
        verite = item["verite"].upper().replace(" ", "").replace("-", "")

        img = cv2.imread(chemin)
        if img is None:
            print(f"Image illisible : {chemin}")
            continue

        img_pretraitee = preproc.pretraiter(img)

        r_easy = easy.lire(img_pretraitee)
        r_tess = tess.lire(img_pretraitee)

        easy_norm = validateur.normaliser(r_easy.texteBrut).replace(" ", "").replace("-", "")
        tess_norm = validateur.normaliser(r_tess.texteBrut).replace(" ", "").replace("-", "")

        easy_ok = easy_norm == verite
        tess_ok = tess_norm == verite

        easy_car = taux_par_caractere(easy_norm, verite)
        tess_car = taux_par_caractere(tess_norm, verite)

        if easy_ok:
            easy_exact += 1
        if tess_ok:
            tess_exact += 1
        easy_car_total += easy_car
        tess_car_total += tess_car

        resultats.append({
            "image": chemin,
            "verite": verite,
            "easyocr": {
                "texte": easy_norm,
                "conf": round(r_easy.confOcr, 2),
                "exact_match": easy_ok,
                "taux_caractere": round(easy_car, 2)
            },
            "tesseract": {
                "texte": tess_norm,
                "conf": round(r_tess.confOcr, 2),
                "exact_match": tess_ok,
                "taux_caractere": round(tess_car, 2)
            }
        })

        print(f"{chemin}")
        print(f"  Verite    : {verite}")
        print(f"  EasyOCR   : '{easy_norm}'  exact={easy_ok}  car={easy_car:.0%}")
        print(f"  Tesseract : '{tess_norm}'  exact={tess_ok}  car={tess_car:.0%}")

    n = len(resultats)
    if n == 0:
        print("Aucune image valide.")
        return {}

    rapport = {
        "nb_images": n,
        "easyocr": {
            "taux_exact_match": round(easy_exact / n * 100, 1),
            "taux_par_caractere": round(easy_car_total / n * 100, 1)
        },
        "tesseract": {
            "taux_exact_match": round(tess_exact / n * 100, 1),
            "taux_par_caractere": round(tess_car_total / n * 100, 1)
        },
        "detail": resultats
    }

    print(f"\n{'='*50}")
    print(f"RAPPORT FINAL — {n} images testées")
    print(f"{'='*50}")
    print(f"EasyOCR   : exact match = {rapport['easyocr']['taux_exact_match']}%  |  taux/caractère = {rapport['easyocr']['taux_par_caractere']}%")
    print(f"Tesseract : exact match = {rapport['tesseract']['taux_exact_match']}%  |  taux/caractère = {rapport['tesseract']['taux_par_caractere']}%")

    with open("ocr/rapport_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    print(f"\nRapport sauvegardé : ocr/rapport_evaluation.json")

    return rapport


if __name__ == "__main__":
    with open("ocr/verite_terrain.json", "r", encoding="utf-8") as f:
        jeu_de_test = json.load(f)
    evaluer(jeu_de_test)
