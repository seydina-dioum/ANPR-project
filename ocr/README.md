# Module OCR — Reconnaissance de texte sur plaques

## Jalon 1 — Installation et premiers tests (terminé)

**Environnement installé :**
- easyocr, pytesseract, opencv-python, Pillow
- Binaire Tesseract 5.5.0 (UB Mannheim), configuré via `tesseract_cmd`

**Classes créées :**
- `ocr_engine.py` : interface `OcrEngine`, implémentations `EasyOcrEngine` et `TesseractEngine`
- `validator.py` : `Validateur` (whitelist, normalisation, validation regex), énumération `Verdict`

**Test sur 5 images génériques (en attendant le dataset sénégalais, sur instruction de l'encadrant) :**

| Image | EasyOCR | Confiance | Tesseract | Verdict |
|---|---|---|---|---|
| plaque1 | OLD-200 | 0.98 | (vide) | DOUTEUSE |
| plaque2 | 00135 | 0.49 | (vide) | DOUTEUSE |
| plaque3 | GBZ | 0.99 | (vide) | ILLISIBLE |
| plaque4 | 86 | 0.42 | (vide) | ILLISIBLE |
| plaque5 | com | 1.00 | (vide) | ILLISIBLE |

**Constat :** EasyOCR détecte toujours du texte (parfois fragmenté), Tesseract ne lit rien sans prétraitement ni cadrage serré.

## Jalon 2 — Prétraitement (terminé)

**Classe créée :**
- `preprocessor.py` : classe `Preprocesseur` avec 5 méthodes (`pretraiter`, `redresser`, `niveauxGris`, `binariser`, `reduireBruit`)

**Test crop serré vs image brute (plaque3) :**

| | Image brute | Crop serré + prétraitement |
|---|---|---|
| EasyOCR | GBZ (0.99) | 691409 (0.61) |
| Tesseract | (vide) | G91409 (0.40) |
| Verdict | ILLISIBLE | DOUTEUSE |

**Conclusions :**
- Le prétraitement fonctionne correctement sur un crop serré
- Tesseract devient utilisable dès que l'image est bien cadrée
- Les deux moteurs convergent sur 5/6 caractères identiques
- plaque4 (plaque sale + rouille) illustre un cas limite documenté dans le cahier des charges

## Jalon 3 — Intégration pipeline complet (à venir)

_À compléter._

## Jalon 3 — Pipeline complet (terminé)

**Fichier créé :**
- `pipeline.py` : classe `PipelineANPR` qui enchaîne détection (YOLOv8) → prétraitement → OCR → validation → JSON

**Structure de la réponse produite :**
```json
{
  "plaques": [
    {
      "texte": "AA-123-BC",
      "texte_brut": "AA 123 BC",
      "bbox": [x1, y1, x2, y2],
      "score_detection": 0.94,
      "conf_ocr": 0.88,
      "valide": true,
      "verdict": "VALIDE"
    }
  ],
  "nb_plaques": 1,
  "temps_ms": 180
}
```

**Test avec modèle générique `yolov8n.pt` :** pipeline tourne sans erreur, 0 détection attendue (modèle non entraîné sur plaques). À retester avec `anpr_best.pt` dès réception du fichier corrigé.
