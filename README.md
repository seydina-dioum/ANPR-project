# ANPR Sénégal — Reconnaissance automatique de plaques d'immatriculation

Projet de stage — École Supérieure Polytechnique (ESP-UCAD), Dakar, Sénégal
Encadrants : Ousseynou Ndour & Souleymane Seck
Équipe : Adji Deguene Diagne (coordinatrice), Membre A (détection), Membre C (API)

## Description

Système ANPR basé sur YOLOv8 + EasyOCR/Tesseract.
À partir d'une image contenant un véhicule, le système détecte la plaque, lit le texte et valide le format sénégalais.

## Lancer l'application

    uvicorn api.main:app --reload

Ouvrez ensuite http://127.0.0.1:8000 dans votre navigateur.

## Installation

1. Cloner le repo : git clone https://github.com/seydina-dioum/ANPR-project.git
2. Créer le venv : python -m venv venv
3. Activer : source venv/Scripts/activate (Windows) ou source venv/bin/activate (Linux/macOS)
4. Installer : pip install -r requirements.txt
5. Installer Tesseract (Windows) : https://github.com/UB-Mannheim/tesseract/wiki
6. Placer le modèle : detection/models/anpr_best.pt (fichier lourd, non inclus dans le repo)

## Structure du projet

- api/          : API REST FastAPI
- detection/    : Module détection YOLOv8 (Membre A)
- ocr/          : Module OCR + validation (Adji Deguene Diagne)
- frontend/     : Interface web (HTML/CSS/JS)
- data/         : Données et dataset
- tests/        : Tests

## Résultats évaluation OCR (Jalon 4)

Jeu de test : 20 images de plaques

| Moteur    | Exact match | Taux par caractère |
|-----------|-------------|-------------------|
| EasyOCR   | 15% (3/20)  | 51.6%             |
| Tesseract | 10% (2/20)  | 51.2%             |

Conclusion : EasyOCR recommandé.

## Formats sénégalais supportés

- Format récent SIM : SN 00-AAA-000
- Format ancien régional : DK 1234, TH 567, etc.
- Deux-roues : A 123 BC

## Notes importantes

- anpr_best.pt non inclus dans le repo (trop lourd) — à placer dans detection/models/
- Images de test exclues par .gitignore
- Application sur CPU — environ 5s par image (GPU recommandé en production)
