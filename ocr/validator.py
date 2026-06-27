import re
from typing import Tuple

WHITELIST = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

PATTERNS = [
    r"^[A-Z]{2}-\d{3,4}-[A-Z]{2}$",
    r"^[A-Z]{2}\d{3,4}[A-Z]{2}$",
]

def normalize(texte_brut: str) -> str:
    texte = texte_brut.upper().strip()
    texte = "".join(c for c in texte if c in WHITELIST or c in "- ")
    texte = re.sub(r"\s+", "-", texte)
    return texte

def validate_plate_sn(texte_brut: str) -> Tuple[str, bool]:
    texte_normalise = normalize(texte_brut)
    for pattern in PATTERNS:
        if re.match(pattern, texte_normalise):
            return texte_normalise, True
    return texte_normalise, False