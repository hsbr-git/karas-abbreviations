import json
import os
import sys
import yaml
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.conjugators.verb import VerbConjugator
from src.conjugators.adjective import AdjectiveConjugator
from src.conjugators.auxiliary import AuxiliaryConjugator

LEFT_THUMB_KEYS = ['A', 'O']
RIGHT_THUMB_KEYS = ['E', 'U']

def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_dictionary():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rules_dir = os.path.join(base_dir, "rules")
    
    # Load common rules
    common_cfg = load_yaml(os.path.join(rules_dir, "common.yaml"))
    left_to_row = common_cfg.get("left_to_row", {})
    right_suffix_to_class = common_cfg.get("right_suffix_to_class", {})
    thumb_actions = common_cfg.get("thumb_actions", {})

    custom_cfg = load_yaml(os.path.join(rules_dir, "custom_rules.yaml"))
    unified_entries = custom_cfg.get("custom_entries") or []
    all_tables = custom_cfg.get("tables") or {}
    phrase_patterns = custom_cfg.get("phrase_patterns") or []

    output_data = {}

    # Initialize conjugators
    verb_conjugator = VerbConjugator(LEFT_THUMB_KEYS, RIGHT_THUMB_KEYS)
    adj_conjugator = AdjectiveConjugator(LEFT_THUMB_KEYS, RIGHT_THUMB_KEYS)
    aux_conjugator = AuxiliaryConjugator(LEFT_THUMB_KEYS, RIGHT_THUMB_KEYS)

    # Dictionary mapping type to conjugator instance
    conjugators = {
        'verb': verb_conjugator,
        'adj': adj_conjugator,
        'auxiliary': aux_conjugator,
    }

    # 1. Process regular verb rows based on left_to_row
    effective_rows = list(left_to_row.items())
    if ("", "") not in effective_rows:
        effective_rows.append(("", ""))

    for left_consonant, row in effective_rows:
        for right_suffix, klass in right_suffix_to_class.items():
            t_klass = all_tables.get(klass)
            if not t_klass or row not in t_klass:
                continue

            for thumb_chord, action in thumb_actions.items():
                romaji = verb_conjugator.conjugate(action, row, klass, all_tables)
                if not romaji:
                    continue
                stroke = verb_conjugator.build_stroke_key(left_consonant, thumb_chord, right_suffix)
                output_data[stroke] = f"{{^{romaji}^}}"

    # 2. Process all custom entries dispatched by 'type'
    # Adding phrase patterns to the loop
    for info in unified_entries + phrase_patterns:
        entry_type = info.get("type", "verb")
        conjugator = conjugators.get(entry_type)

        if not conjugator:
            print(f"Warning: Unknown entry type '{entry_type}' for entry {info}")
            continue

        left_stroke = info.get("left_stroke", "")
        right_stroke = info.get("right_stroke", "")
        stem = info.get("stem", "")
        row = info.get("row", "")
        klass = info.get("class", "")
        bindings = info.get("bindings", {})
        allowed = info.get("allowed_kinds")

        # Dispatch based on type
        if entry_type == 'verb':
            t_klass = all_tables.get(klass)
            if not t_klass or row not in t_klass:
                continue

            for thumb_chord, action in thumb_actions.items():
                if allowed is not None and action["kind"] not in allowed:
                    continue
                romaji = conjugator.conjugate(action, row, klass, all_tables, stem=stem)
                if not romaji:
                    continue
                stroke = conjugator.build_stroke_key(left_stroke, thumb_chord, right_stroke)
                output_data[stroke] = f"{{^{romaji}^}}"
        
        elif entry_type == 'adj':
            # Adjectives might not depend on a 'row' or 't_klass' from verb tables (adj tables not needed yet)
            for thumb_chord, action in thumb_actions.items():
                if allowed is not None and action["kind"] not in allowed:
                    continue
                romaji = conjugator.conjugate(action, row, klass, all_tables, stem=stem)
                if not romaji:
                    continue
                stroke = conjugator.build_stroke_key(left_stroke, thumb_chord, right_stroke)
                output_data[stroke] = f"{{^{romaji}^}}"

        elif entry_type == 'auxiliary':
            for thumb_chord, action in thumb_actions.items():
                if allowed is not None and action["kind"] not in allowed:
                    continue
                romaji = conjugator.conjugate(action, row, klass, all_tables, stem=stem)
                if not romaji:
                    continue
                stroke = conjugator.build_stroke_key(left_stroke, thumb_chord, right_stroke)
                output_data[stroke] = f"{{^{romaji}^}}"

        elif entry_type == 'phrase':
            # Phrases skip the standard `action["kind"]` matrix entirely
            for thumb_chord, romaji in bindings.items():
                if not romaji:
                    continue
                stroke = phrase_conjugator.build_stroke_key(left_stroke, thumb_chord, right_stroke)
                output_data[stroke] = f"{{^{romaji}^}}"

    return output_data

def save_as_json(data, file_path):
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Successfully saved JSON data to: {file_path}")
    except Exception as e:
        print(f"❌ An error occurred while saving the file: {e}")

if __name__ == "__main__":
    output_data = generate_dictionary()
    
    # Save slightly differently named purely to verify parity before swapping
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "verb.json"))
    save_as_json(output_data, output_file_path)
    print(f"Generated data to {output_file_path}")
