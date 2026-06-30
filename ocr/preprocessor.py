import cv2
import numpy as np


class Preprocesseur:

    def niveauxGris(self, img):
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def reduireBruit(self, img):
        return cv2.medianBlur(img, 3)

    def binariser(self, img):
        _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img_bin

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
        img = self.niveauxGris(img)
        img = self.reduireBruit(img)
        img = self.binariser(img)
        return img
