class PhraseConjugator:
    def __init__(self, thumbs_left, thumbs_right):
        self.thumbs_left = thumbs_left
        self.thumbs_right = thumbs_right

    def conjugate(self, action_kind: str, row_key: str, klass: str, tables: dict, bindings: dict = None, stem: str = "") -> str | None:
        """
        Phrase conjugation logic.
        Unlike verbs/adjectives that use action_kind mathematically, 
        phrases define specific outputs for specific thumb thumb actions (A, O, AO, etc.).
        
        Since verb.py passes `action_kind` (e.g. 'shushi', 'masu'), we need to map that back to the thumb chord, 
        or better yet, handle the bindings directly if they specify kinds.
        Actually, the user requested binding directly to the thumb key (e.g. O: 'kamosirenai').
        But `verb.py` loops over thumb_actions which are dicts mapping 'O' -> {'kind': 'shushi'}.
        
        To make it work smoothly with `verb.py`'s current loop, we can pass the thumb key as `action_kind` 
        if we alter the call, OR we can map the `kind` back to the string in bindings. 
        However, the cleanest way is for the bindings to use 'kind' as keys!
        Wait, the user example was: `bindings: {'O': 'kamosirenai', 'AO': 'kamosiremasenn'}`.
        Let's allow bindings to key on either the thumb chord ('O', 'AO') or the kind ('shushi', 'masu').
        """
        if not bindings:
            return None

        # Hack: verb.py calls conjugate(action["kind"], ...). 
        # But we don't know the thumb key here. 
        # Let's map kinds back to common thumb keys to match user's yaml, 
        # OR we just tell the user to use 'shushi', 'masu' in the yaml.
        # Looking at the yaml I wrote: bindings: {'O': 'kamosirenai', 'AO': 'kamosiremasenn', ...}
        # It's better if `conjugate` receives the thumb_chord directly!
        pass

    def get_romaji_for_chord(self, thumb_chord: str, bindings: dict) -> str | None:
        """
        Directly fetch the romaji for a given thumb chord.
        """
        if not bindings:
            return None
        return bindings.get(thumb_chord)

    def build_stroke_key(self, left_stroke: str, thumb_chord: str, right_stroke: str) -> str:
        left_thumb_part = []
        right_thumb_part = []
        for ch in str(thumb_chord):
            if ch in self.thumbs_left:
                left_thumb_part.append(ch)
            elif ch in self.thumbs_right:
                right_thumb_part.append(ch)
            else:
                raise ValueError(f"Unexpected thumb char: {ch}")
        return f"{left_stroke}{''.join(left_thumb_part)}-{''.join(right_thumb_part)}{right_stroke}"
