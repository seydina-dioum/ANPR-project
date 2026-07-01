from ultralytics import YOLO
import os


class Evaluateur:

    def __init__(self, modele_path="detection/models/anpr_best.pt", data_yaml="data/dataset/data.yaml"):
        self.modele_path = modele_path
        self.data_yaml = data_yaml
        self.modele = YOLO(modele_path)

    def calculer_map(self):
        resultats = self.modele.val(
            data=self.data_yaml,
            split="test",
            verbose=False
        )
        map50 = round(resultats.box.map50, 4)
        map50_95 = round(resultats.box.map, 4)
        print(f"mAP50     : {map50}")
        print(f"mAP50-95  : {map50_95}")
        return map50, map50_95


if __name__ == "__main__":
    e = Evaluateur()
    e.calculer_map()