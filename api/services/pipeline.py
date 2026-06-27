from typing import List
from api.models.schemas import PlaquResult
from api.utils.image import bytes_to_cv2

async def run_pipeline(image_bytes: bytes) -> List[PlaquResult]:
    # Pipeline complet sera connecté ici
    # quand le Membre A (YOLOv8) et Membre B (OCR) auront fini
    image = bytes_to_cv2(image_bytes)
    return []