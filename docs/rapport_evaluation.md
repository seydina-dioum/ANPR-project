# Rapport d'évaluation — Détection de plaques (YOLOv8)

Membre A — Jalon 4

---

Introduction

Dans le cadre de notre projet ANPR, ma partie consistait à mettre en
place la détection des plaques d'immatriculation avec YOLOv8. Ce rapport
présente les tests effectués, les résultats obtenus et les difficultés
rencontrées pendant le développement.

---

Dataset utilisé

Source : Roboflow Universe — License Plate Computer Vision Model
Licence : CC BY 4.0 (libre d'utilisation)
Total images : 366 annotées avec bounding boxes autour des plaques
Répartition : train 219 / valid 76 / test 71
Classes : Plate-Number et Invalid plate

---

Test du modèle pré-entraîné

Avant le fine-tune, j'ai testé le modèle yolov8n.pt tel quel sur
10 images pour avoir une base de comparaison.

Image Résultat Confiance Classe détectée
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

Deux problèmes ont été identifiés :
Le modèle détectait des classes génériques comme truck ou car
au lieu de Plate-Number. C'est normal car yolov8n.pt est entraîné
sur 80 classes génériques et ne connaît pas les plaques.
Sur IMG_2953, il y avait 7 détections pour une seule plaque réelle,
ce qui montre beaucoup de faux positifs.

Décision prise : fine-tune nécessaire sur notre dataset de plaques.

---

Fine-tuning

Paramètres utilisés pour l'entraînement :
Modèle de base : yolov8n.pt
Epochs : 30
Image size : 640x640
Batch size : 8
Durée : environ 4 heures sur CPU (Intel Core i7-8665U, pas de GPU)
Modèle produit : anpr_best.pt (6.2 MB)

Résultats sur le jeu de validation :

Métrique Valeur
Précision 90.0%
Rappel 91.2%
mAP50 94.4%
mAP50-95 79.5%

---

Évaluation officielle sur le jeu de test

Les résultats officiels ont été calculés sur les 71 images du jeu
de test avec la classe Evaluateur développée dans evaluateur.py.

Métrique Validation Test officiel
Précision 90.0% 98.8%
Rappel 91.2% 43.2%
mAP50 94.4% 46.0%
mAP50-95 79.5% 37.2%

---

Analyse de l'écart validation / test

La précision est excellente à 98.8%, ce qui veut dire que quand
le modèle détecte une plaque, il se trompe rarement.

Le rappel est faible à 43.2%, ce qui veut dire que le modèle rate
environ 57% des plaques dans le jeu de test.

Cet écart s'explique par le fait que le jeu de test contient des
images plus difficiles que celles vues pendant l'entraînement.
30 epochs sur 219 images ne suffisent pas pour bien généraliser
sur toutes les conditions réelles.

---

Cas difficiles observés

Angle supérieur à 30 degrés — le modèle rate souvent la plaque
quand la photo est prise de côté.

Image sombre ou de nuit — les confiances tombent en dessous de 0.3,
les détections sont peu fiables.

Plaque sale ou abîmée — les plaques avec de la boue ou détériorées
sont difficiles à localiser.

Véhicule trop loin — quand la plaque est trop petite dans l'image,
le modèle ne la détecte pas.

---

Comparaison avant / après fine-tune

                    Avant fine-tune     Après fine-tune

Taux détection 80% 93%
Classes reconnues truck, car... Plate-Number
Faux positifs Nombreux Très peu
Confiance moyenne ~0.60 ~0.88
mAP50 — 94.4%

Le fine-tune a clairement amélioré les résultats même si le rappel
sur le jeu de test reste à améliorer.

---

Recommandations

Augmenter le nombre d'epochs à 50 ou 100 pour donner plus de temps
au modèle pour apprendre les différents cas.

Enrichir le dataset avec des images de plaques sénégalaises
spécifiques : format SIM récent, deux-roues, plaques administratives
et diplomatiques. 30 images ont déjà été collectées, l'annotation
est en cours sur Roboflow.

Baisser le seuil de confiance de 0.5 à 0.3 pour réduire les
non-détections sur les cas difficiles.

Utiliser un GPU NVIDIA pour l'entraînement : 4 heures sur CPU
se réduiraient à 15-20 minutes, ce qui permettrait de tester
plus de configurations.

Appliquer de l'augmentation de données : rotation, changement de
luminosité, flou artificiel pour rendre le modèle plus robuste
aux conditions réelles de terrain.
