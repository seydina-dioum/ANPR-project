from ultralytics import YOLO
import cv2
import os


class DetecteurYOLO:

    def __init__(self, modele_path="detection/models/anpr_best.pt", seuil=0.5):
        self.modele_path = modele_path
        self.seuil = seuil
        self.modele = None

    def charger_modele(self):
        if not os.path.exists(self.modele_path):
            print("modele introuvable")
            return False
        self.modele = YOLO(self.modele_path)
        print("modele charge")
        return True

    def detecter(self, image):
        if self.modele is None:
            print("charge le modele dabord")
            return []
        results = self.modele(image, verbose=False)
        bboxes = []
        for r in results:
            for box in r.boxes:
                b = {
                    "x1": int(box.xyxy[0][0]),
                    "y1": int(box.xyxy[0][1]),
                    "x2": int(box.xyxy[0][2]),
                    "y2": int(box.xyxy[0][3]),
                    "confiance": round(float(box.conf), 4),
                    "classe": r.names[int(box.cls)]
                }
                bboxes.append(b)
        return bboxes

    def filtrer(self, bboxes, seuil=None):
        if seuil is None:
            seuil = self.seuil
        return [b for b in bboxes if b["confiance"] >= seuil]

    def decouper(self, image, bbox):
        if isinstance(image, str):
            img = cv2.imread(image)
        else:
            img = image
        x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
        h, w = img.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        return img[y1:y2, x1:x2]

    def traiter(self, image):
        bboxes = self.detecter(image)
        bboxes = self.filtrer(bboxes)
        resultats = []
        for bbox in bboxes:
            crop = self.decouper(image, bbox)
            resultats.append({"bbox": bbox, "crop": crop})
        return resultats


if __name__ == "__main__":
    d = DetecteurYOLO()
    d.charger_modele()

    img = "data/dataset/test/images/IMG_2738_png.rf.39e4670d6058377fcb2dfbf265a76924.jpg"
    resultats = d.traiter(img)

    print(f"{len(resultats)} plaque(s) detectee(s)")
    for i, r in enumerate(resultats):
        print(f"plaque {i+1} : {r['bbox']}")
        print(f"crop shape : {r['crop'].shape}")