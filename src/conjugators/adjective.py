class AdjectiveConjugator:
    def __init__(self, thumbs_left, thumbs_right):
        self.thumbs_left = thumbs_left
        self.thumbs_right = thumbs_right

    def conjugate(self, action: dict, row_key: str, klass: str, tables: dict, stem: str = "") -> str | None:
        """
        Adjective conjugation logic.
        Supports 'i_adj' (い形容詞) and 'nai_adj' (ないで終わる助動詞等).
        """
        if klass not in ["i_adj", "nai_adj"]:
            return None

        r = tables.get(klass)
        if not r:
            return None

        # Get adj-specific conjugation instructions
        instr = action.get("adj")
        if not instr:
            return None

        # Handle nai_adj override for polite forms etc. if defined
        if klass == "nai_adj" and "nai_adj_suffix" in instr:
            res = instr["nai_adj_suffix"]
            return stem + res

        base_key = instr.get("base")
        base_form = r.get(base_key)
        if base_form is None:
            return None

        suffix = instr.get("suffix", "")
        
        res = base_form + suffix

        if "None" in str(res):
            return None
        return stem + str(res)
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
