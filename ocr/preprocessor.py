import cv2
import numpy as np


class Preprocesseur:

    def niveauxGris(self, img):
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def reduireBruit(self, img):
        # Filtre bilatéral : réduit le bruit tout en préservant les bords du texte
        return cv2.bilateralFilter(img, 9, 75, 75)

    def binariser(self, img):
        # Seuillage adaptatif : gère mieux les variations d'éclairage que Otsu
        return cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 10
        )

    def redimensionner(self, img, hauteur_cible=64):
        """Redimensionne le crop à une hauteur standard pour normaliser les tailles."""
        h, w = img.shape[:2]
        if h == 0 or w == 0:
            return img
        ratio = hauteur_cible / h
        nouvelle_largeur = int(w * ratio)
        if nouvelle_largeur == 0:
            return img
        return cv2.resize(img, (nouvelle_largeur, hauteur_cible), interpolation=cv2.INTER_CUBIC)

    def ajouter_padding(self, img, padding=16):
        """Ajoute un padding blanc autour du crop pour donner plus de contexte à l'OCR."""
        couleur = 255 if len(img.shape) == 2 else (255, 255, 255)
        return cv2.copyMakeBorder(
            img, padding, padding, padding, padding,
            cv2.BORDER_CONSTANT, value=couleur
        )

    def redresser(self, img):
        gris = self.niveauxGris(img)
        bords = cv2.Canny(gris, 50, 150)
        lignes = cv2.HoughLinesP(bords, 1, np.pi / 180, threshold=50,
                                  minLineLength=img.shape[1] // 3, maxLineGap=10)

        if lignes is None:
            return img

        angles = []
        for ligne in lignes:
            x1, y1, x2, y2 = ligne[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if -45 < angle < 45:
                angles.append(angle)

        if not angles:
            return img

        angle_moyen = np.median(angles)
        (h, w) = img.shape[:2]
        centre = (w // 2, h // 2)
        matrice_rotation = cv2.getRotationMatrix2D(centre, angle_moyen, 1.0)
        return cv2.warpAffine(img, matrice_rotation, (w, h),
                               flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def pretraiter(self, crop):
        img = self.redresser(crop)
        img = self.redimensionner(img)
        img = self.niveauxGris(img)
        img = self.reduireBruit(img)
        img = self.binariser(img)
        img = self.ajouter_padding(img)
        return img
