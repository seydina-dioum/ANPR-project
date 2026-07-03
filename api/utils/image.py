import numpy as np
import cv2

def bytes_to_cv2(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Impossible de décoder l'image.")
    return image