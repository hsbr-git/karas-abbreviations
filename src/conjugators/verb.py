class VerbConjugator:
    def __init__(self, thumbs_left, thumbs_right):
        self.thumbs_left = thumbs_left
        self.thumbs_right = thumbs_right

    def conjugate(self, action: dict, row_key: str, klass: str, tables: dict, stem: str = "") -> str | None:
        t = tables.get(klass)
        if not t:
            return None
        r = t.get(row_key)
        if not r:
            return None

        # Get verb-specific conjugation instructions
        instr = action.get("verb")
        if not instr:
            return None

        base_key = instr.get("base")
        # Support kahen override for base if defined
        if klass == "kahen" and "kahen_base" in instr:
             base_key = instr["kahen_base"]
        
        base_form = r.get(base_key)
        if not base_form:
            return None

        # Special case for "行く" (iku): Use "ltu" onbin instead of "i"
        if klass == "godan" and row_key == "k" and stem == "i" and base_key == "onbin":
            base_form = "ltu"

        suffix = instr.get("suffix", "")
        
        # Handle special case for "ある" (stem 'a', row 'r') + "ない" (kind 'nai') -> "あらず"
        if stem == "a" and row_key == "r" and action.get("kind") == "nai":
            return "arazu"
        if stem == "a" and row_key == "r" and action.get("kind") == "nakatta":
            return "nakatta"

        # Resolve suffixes like {te/de}, {ta/da}, {u/you}
        suffix = self._resolve_suffix(suffix, row_key, klass)

        return stem + base_form + suffix

    def _resolve_suffix(self, suffix: str, row_key: str, klass: str) -> str:
        if "{te/de}" in suffix:
            replacement = "de" if row_key in ("g", "b", "n", "m") else "te"
            suffix = suffix.replace("{te/de}", replacement)
        if "{ta/da}" in suffix:
            replacement = "da" if row_key in ("g", "b", "n", "m") else "ta"
            suffix = suffix.replace("{ta/da}", replacement)
        if "{u/you}" in suffix:
            replacement = "you" if klass in ("kami_ichidan", "shimo_ichidan", "sahen", "kahen") else "u"
            suffix = suffix.replace("{u/you}", replacement)
        return suffix

    def build_stroke_key(self, left_consonant: str, thumb_chord: str, right_stroke: str) -> str:
        left_thumb_part = []
        right_thumb_part = []
        for ch in str(thumb_chord):
            if ch in self.thumbs_left:
                left_thumb_part.append(ch)
            elif ch in self.thumbs_right:
                right_thumb_part.append(ch)
            else:
                raise ValueError(f"Unexpected thumb char: {ch}")
        return f"{left_consonant}{''.join(left_thumb_part)}-{''.join(right_thumb_part)}{right_stroke}"
