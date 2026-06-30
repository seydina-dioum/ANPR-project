# Module Détection — YOLOv8

Jalon 1 — Mise en place (terminé)

Environnement installé :
Python 3.13.9 avec environnement virtuel (venv)
ultralytics 8.4.80, opencv-python, torch 2.12.1, torchvision
Modèle pré-entraîné téléchargé : yolov8n.pt (6.2 MB)

Gestion du dépôt GitHub :
Dépôt créé : github.com/seydina-dioum/ANPR-project
Structure des dossiers mise en place : detection/, ocr/, api/,
client/, data/, tests/, docs/
5 branches créées : main, dev, feature/detection, feature/ocr, feature/api
Branches main et dev protégées (Pull Request obligatoire)
README.md complet et licence AGPL-3.0 officiels ajoutés
Membres B et C invités comme collaborateurs

Dataset collecté :
Source : Roboflow Universe — License Plate Computer Vision Model
Licence : CC BY 4.0
366 images annotées avec bounding boxes autour des plaques
Répartition : train 219 / valid 76 / test 71
Classes : Plate-Number et Invalid plate

Test du modèle pré-entraîné sur 10 images :

Image EasyOCR Confiance Classe détectée
images-11 Détectée 0.85 truck
images-2 Non détectée — —
images-21 Détectée 0.38 car
images-4 Non détectée — —
images-7 Détectée 0.60 car
IMG_2738 Détectée 0.84 truck
IMG_2948 Détectée 0.74 car
IMG_2950 Détectée 0.81 truck
IMG_2953 Détectée 0.71 truck
IMG_2961 Détectée 0.68 car

Taux de détection : 8/10 = 80%

Constat : le modèle pré-entraîné détecte des objets génériques
(truck, car) au lieu de plaques. Sur IMG_2953, 7 détections pour
une seule plaque réelle — beaucoup de faux positifs.
Décision : fine-tune nécessaire sur notre dataset.

---

Jalon 2 — Développement du module de détection (terminé)

Classe créée :
detector.py : classe DetecteurYOLO avec 5 méthodes
charger_modele() : charge le fichier .pt en mémoire
detecter(image) : retourne toutes les bounding boxes détectées
filtrer(bboxes) : filtre selon le seuil de confiance (défaut 0.5)
decouper(image, bbox) : extrait le crop de la zone plaque
traiter(image) : pipeline complet en un seul appel

Fine-tuning lancé sur notre dataset :
Modèle de base : yolov8n.pt
Epochs : 30
Image size : 640x640
Batch size : 8
Durée : environ 4 heures (CPU Intel Core i7-8665U, pas de GPU)
Modèle produit : anpr_best.pt (6.2 MB)

Résultats sur le jeu de validation après fine-tune :

                    Avant fine-tune     Après fine-tune

Taux détection 80% 93%
Classes reconnues truck, car... Plate-Number
Faux positifs Nombreux Très peu
Confiance moyenne ~0.60 ~0.88
mAP50 — 94.4%
mAP50-95 — 79.5%

Le fine-tune a clairement amélioré les résultats. Le modèle
reconnaît maintenant les plaques correctement au lieu d'objets
génériques.

---

Jalon 3 — Intégration pipeline complet (à venir)

En attente de la partie OCR (Membre B) et API (Membre C)
pour intégrer le module de détection dans le pipeline complet.

---

Jalon 4 — Évaluation (terminé)

Classe créée :
evaluateur.py : classe Evaluateur avec la méthode calculer_map()
qui calcule le mAP50 et mAP50-95 sur le jeu de test officiel.

Résultats officiels sur le jeu de test (71 images) :

Métrique Validation Test officiel
Précision 90.0% 98.8%
Rappel 91.2% 43.2%
mAP50 94.4% 46.0%
mAP50-95 79.5% 37.2%

Constat : la précision est excellente (98.8%) mais le rappel
est faible (43.2%). Le modèle détecte correctement quand il
détecte, mais rate trop de plaques dans le jeu de test.

Explication de l'écart : le jeu de test contient des images
plus difficiles. 30 epochs sur 219 images ne suffisent pas
pour bien généraliser sur toutes les conditions réelles.

Cas difficiles documentés :
Angle supérieur à 30 degrés — plaque non détectée
Image sombre ou de nuit — confiance en dessous de 0.3
Plaque sale ou abîmée — non détectée
Véhicule trop loin — plaque trop petite dans l'image

En cours — Plaques sénégalaises spécifiques :
30 images collectées sur internet couvrant les formats suivants :
Plaques SIM (nouveau format blanc) : environ 15 images
Plaques anciennes (bleues DK, TH...) : environ 12 images
Motos : environ 3 images
Diplomatiques : 0 image (difficile à trouver sur internet)

Annotation en cours sur Roboflow. Un deuxième fine-tune sera
lancé après annotation pour améliorer les performances sur les
plaques sénégalaises spécifiquement.
