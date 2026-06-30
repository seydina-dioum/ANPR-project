from enum import Enum
import re


class Verdict(Enum):
    VALIDE = "VALIDE"
    DOUTEUSE = "DOUTEUSE"
    ILLISIBLE = "ILLISIBLE"


class Validateur:
    def __init__(self):
        self.whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- "
        self.formatsRegex = [
            r"^SN\d{2}-[A-Z]{3}-\d{3}$",
            r"^[A-Z]{2}\d{1,6}$",
            r"^[A-Z]\d{3}[A-Z]{2}$",
        ]

    def _appliquer_whitelist(self, texte: str) -> str:
        return "".join(c for c in texte if c in self.whitelist)

    def normaliser(self, texte: str) -> str:
        texte = texte.upper().strip()
        texte = self._appliquer_whitelist(texte)
        texte = re.sub(r"\s+", "", texte)
        return texte

    def valider(self, texte: str) -> Verdict:
        normalise = self.normaliser(texte)
        if len(normalise) < 5:
            return Verdict.ILLISIBLE
        for pattern in self.formatsRegex:
            if re.match(pattern, normalise):
                return Verdict.VALIDE
        return Verdict.DOUTEUSE
