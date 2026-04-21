class AuxiliaryConjugator:
    def __init__(self, thumbs_left, thumbs_right):
        self.thumbs_left = thumbs_left
        self.thumbs_right = thumbs_right

    def conjugate(self, action: dict, row_key: str, klass: str, tables: dict, stem: str = "") -> str | None:
        t = tables.get(klass)
        if not isinstance(t, dict):
            return None

        instr_all = action.get("auxiliary")
        if not instr_all:
            return None

        # Supports both:
        # auxiliary: {base: shushi, suffix: "..."}
        # auxiliary: {da_auxiliary: {...}, desu_auxiliary: {...}}
        if "base" in instr_all or "suffix" in instr_all:
            instr = instr_all
        else:
            instr = instr_all.get(klass) or instr_all.get("default")
            if not instr:
                return None

        base_key = instr.get("base")
        if not base_key:
            return None

        base_form = t.get(base_key)
        if base_form is None:
            return None

        suffix = instr.get("suffix", "")
        return stem + str(base_form) + str(suffix)

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
