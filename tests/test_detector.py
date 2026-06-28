from detection.detector import DetecteurYOLO
import os

d = DetecteurYOLO()
d.charger_modele()

images = os.listdir("data/dataset/test/images")[:10]

ok = 0
echec = 0

for img_name in images:
    img_path = f"data/dataset/test/images/{img_name}"
    resultats = d.traiter(img_path)
    if len(resultats) > 0:
        ok += 1
        print(f"OK  {img_name[:40]} → {len(resultats)} plaque(s)")
    else:
        echec += 1
        print(f"NON {img_name[:40]} → rien detecte")

print(f"\nTotal : {ok} detectees, {echec} ratees sur 10")