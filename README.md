**# ANPR — Reconnaissance Automatique de Plaques d'Immatriculation**



**Système de détection et lecture automatique de plaques d'immatriculation**

**développé dans le cadre d'un projet de stage.**



**> Encadrants : Ousseynou Ndour \& Souleymane Seck**

**> Responsable : Adji Deguene Diagne**

**> Version 1.0 — Juin 2026**



**---**



**## Contexte**



**Ce projet est un produit générique proposé par l'entreprise. Il expose**

**un service de lecture de plaques via une API REST que le client peut**

**brancher sur son propre besoin : contrôle d'accès de parking, barrière**

**automatique, péage, gestion de flotte, surveillance, statistiques de**

**trafic, etc.**



**Le périmètre de l'équipe est le moteur ANPR + son API, pas une**

**application métier finale.**



**---**



**## Chaîne de traitement**

**Image (upload API ou capture webcam)**



**│**



**▼**



**┌─────────────────────────┐**



**│  1. YOLOv8 (détection)  │  → localise la/les plaque(s) + bbox**



**└────────────┬────────────┘**



**│**



**▼**



**┌─────────────────────────┐**



**│  2. EasyOCR / Tesseract │  → lit le texte de chaque plaque**



**└────────────┬────────────┘**



**│**



**▼**



**┌─────────────────────────┐**



**│  3. Validation format   │  → normalise et valide (format SN)**



**└────────────┬────────────┘**



**│**



**▼**



**JSON structuré retourné au client**



**---**



**## Périmètre MVP**



**### Inclus**

**- Entrée par image (upload via API ; webcam dans le client de démo)**

**- Détection d'une ou plusieurs plaques par image (YOLOv8)**

**- OCR du texte de chaque plaque détectée**

**- Post-traitement : whitelist de caractères, normalisation,**

&#x20; **validation du format de plaque sénégalaise**

**- API REST renvoyant le résultat en JSON**

**- Client web de démo (upload / webcam)**

**- Évaluation : mAP de détection, taux de plaques exactes,**

&#x20; **comparaison EasyOCR vs Tesseract**



**### Hors MVP (niveaux supérieurs)**

**- Traitement de flux vidéo / RTSP**

**- Temps réel embarqué (edge / caméra)**

**- Toute application métier (barrière, facturation, alertes)**

**- Reconnaissance du type / marque / couleur du véhicule**



**---**



**## Architecture**

**Client / Demo web**



**\[ Upload image ou webcam (getUserMedia) ]**



**│**



**│ image (HTTP, multipart)**



**▼**



**\[ API ANPR — service Docker ]**



**YOLOv8 (détection)**

**EasyOCR / Tesseract (OCR)**

**Validation format**



**│**



**│ JSON : plaques \[{texte, bbox, scores}]**



**▼**



**Affichage / consommation par le client**





**---**



**## Structure du projet**

**ANPR-project/**



**├── detection/          # Membre A — Détection YOLOv8**



**├── ocr/                # Membre B — OCR + Validation format**



**├── api/                # Membre C — API REST FastAPI**



**├── client/             # Membre C — Client web de démo**



**├── data/               # Images de test et annotations**



**├── tests/              # Tests unitaires**



**├── docs/               # Documentation et rapport d'évaluation**



**├── Dockerfile**



**├── docker-compose.yml**



**├── requirements.txt**



**└── README.md**



**---**



**## Installation**



**### Prérequis**

**- Python 3.10+**

**- Git**

**- Tesseract OCR (binaire système)**

&#x20; **- Windows : https://github.com/UB-Mannheim/tesseract/wiki**

&#x20; **- Linux : `sudo apt install tesseract-ocr`**



**### Environnement Python**



**```bash**

**# Cloner le repo**

**git clone https://github.com/seydina-dioum/ANPR-project.git**

**cd ANPR-project**



**# Créer l'environnement virtuel**

**python -m venv venv**



**# Activer (Windows)**

**venv\\Scripts\\activate**



**# Activer (Linux / Mac)**

**source venv/bin/activate**



**# Installer les dépendances**

**pip install -r requirements.txt**

**```**



**### Dépendances principales**

**ultralytics       # YOLOv8**



**easyocr           # OCR moteur 1**



**pytesseract       # OCR moteur 2 (wrapper Python Tesseract)**



**opencv-python     # Traitement d'image**



**fastapi           # API REST**



**uvicorn           # Serveur ASGI**



**torch             # Requis par YOLOv8**



**Pillow            # Manipulation d'images**



**---**



**## Lancer l'API**



**```bash**

**uvicorn api.main:app --reload**

**```**



**| Endpoint  | Méthode | Description                            |**

**|-----------|---------|----------------------------------------|**

**| `/detect` | POST    | Image en entrée → plaques lues en JSON |**

**| `/health` | GET     | Vérification que le service est en ligne |**



**### Exemple de réponse JSON**



**```json**

**{**

&#x20; **"plaques": \[**

&#x20;   **{**

&#x20;     **"texte": "AA-123-BC",**

&#x20;     **"texte\_brut": "AA 123 BC",**

&#x20;     **"bbox": \[412, 290, 560, 340],**

&#x20;     **"score\_detection": 0.94,**

&#x20;     **"conf\_ocr": 0.88,**

&#x20;     **"valide": true**

&#x20;   **}**

&#x20; **],**

&#x20; **"nb\_plaques": 1,**

&#x20; **"temps\_ms": 180**

**}**

**```**



**---**



**## Organisation de l'équipe**



**| Membre | Responsabilité principale |**

**|---|---|**

**| \*\*Membre A\*\* | Détection : données, YOLOv8, fine-tune, évaluation mAP |**

**| \*\*Membre B\*\* | OCR : EasyOCR vs Tesseract, prétraitement, validation format SN |**

**| \*\*Membre C\*\* | API REST + client web de démo + packaging Docker |**



**---**



**## Convention de branches**



**| Branche | Responsable | Contenu |**

**|---|---|---|**

**| `main` | — | Version finale stable (ne pas toucher directement) |**

**| `dev` | Tous | Branche d'intégration commune |**

**| `feature/detection` | Membre A | YOLOv8, détection, évaluation mAP |**

**| `feature/ocr` | Membre B | OCR, prétraitement, validation format |**

**| `feature/api` | Membre C | API REST, client web, Docker |**



**---**



**## Workflow Git**



**```bash**

**# Avant de commencer à coder**

**git checkout feature/MA-BRANCHE**

**git pull origin dev**



**# Sauvegarder son travail**

**git add .**

**git commit -m "feat: description de ce que j'ai fait"**

**git push origin feature/MA-BRANCHE**



**# Quand un module est terminé**

**# → ouvrir une Pull Request vers dev depuis GitHub**

**```**



**---**



**## Planning (jalons)**



**| Jalon | Objectif | Critère de validation |**

**|---|---|---|**

**| \*\*J1\*\* | Cadrage + inventaire données + test modèle pré-entraîné | Détection visible sur une vraie plaque sénégalaise |**

**| \*\*J2\*\* | Pipeline détection + OCR de bout en bout | Une image → plaque(s) lue(s) en console |**

**| \*\*J3\*\* | Validation format + API REST + client web | Appel API → JSON ; démo affiche la plaque |**

**| \*\*J4\*\* | Évaluation + robustesse + démo finale | Tableau de résultats + démo prête |**



**---**



**## Livrables attendus**



**1. Jeu de test annoté de plaques + protocole d'évaluation**

**2. Code source (dépôt Git) : moteur ANPR + API + client de démo**

**3. API fonctionnelle : image → détection → OCR → validation → JSON**

**4. Client web de démo : upload / webcam → affichage des plaques**

**5. Rapport d'évaluation : mAP, taux de lecture, comparaison**

&#x20;  **EasyOCR vs Tesseract, choix justifiés, difficultés**

**6. Démonstration sur de vraies images de véhicules sénégalais**



**---**



**## Critères d'acceptation (MVP)**



**- L'API détecte la/les plaque(s) et renvoie leurs bbox**

**- Le texte de chaque plaque est lu et normalisé (format sénégalais)**

**- La réponse JSON contient texte, position et indices de confiance**

**- Le client web permet upload / webcam et affiche le résultat**

**- Un rapport compare EasyOCR et Tesseract avec des chiffres**

**- Les erreurs sont gérées (aucune plaque, image illisible,**

&#x20; **service indisponible)**



**---**



**## Licence et point de vigilance commercial**



**| Outil | Licence | Contrainte |**

**|---|---|---|**

**| YOLOv8 (Ultralytics) | AGPL-3.0 |  Voir ci-dessous |**

**| EasyOCR | Apache-2.0 | Aucune contrainte |**

**| Tesseract | Apache-2.0 | Aucune contrainte |**



**\*\* Point à clarifier avec l'entreprise avant industrialisation :\*\***

**YOLOv8 est sous licence AGPL-3.0. Pour un produit commercial distribué,**

**cela impose soit la conformité AGPL (publication du code source), soit**

**l'achat d'une licence commerciale auprès d'Ultralytics.**

**Sans incidence pour le prototype de stage, mais doit être documenté.**



**> Source : Cahier des charges ANPR — Section 1, point 1.**

**>Voir le fichier \[LICENSE](LICENSE) pour le texte complet.**

