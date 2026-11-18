import json
import os
import yaml

LEFT_THUMB_KEYS = ["A", "O"]
RIGHT_THUMB_KEYS = ["E", "U"]


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_as_json(data, file_path):
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Successfully saved JSON data to: {file_path}")
    except Exception as e:
        print(f"❌ An error occurred while saving the file: {e}")


def compose_stroke(base_stroke: str = "", thumb_chord: str = "") -> str:
    if "-" in base_stroke:
        left_base, right_base = base_stroke.split("-", 1)
    else:
        left_base, right_base = base_stroke, ""

    left_thumb_part = []
    right_thumb_part = []
    for ch in str(thumb_chord):
        if ch in LEFT_THUMB_KEYS:
            left_thumb_part.append(ch)
        elif ch in RIGHT_THUMB_KEYS:
            right_thumb_part.append(ch)
        else:
            raise ValueError(f"Unexpected thumb char: {ch}")

    left_side = f"{left_base}{''.join(left_thumb_part)}"
    right_side = f"{''.join(right_thumb_part)}{right_base}"
    return f"{left_side}-{right_side}"


def generate_particle_dictionary():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(base_dir, "rules", "particle.yaml")
    cfg = load_yaml(rules_path) or {}

    first_particles = cfg.get("first_particles") or {}
    second_particles = cfg.get("second_particles") or {}
    matrix = cfg.get("matrix") or {}
    overrides = cfg.get("overrides") or {}
    additional_entries = cfg.get("additional_entries") or []

    output_data = {}

    # 1) 二文字目助詞は親指単打の一文字助詞としても使う。
    # first_particles 側のストロークが空の場合は、後段で
    # 「親指単打（row_stroke）のみ」を使った生成になる。
    for particle in second_particles.values():
        stroke = compose_stroke("", particle.get("stroke", ""))
        text = particle.get("text", "")
        if stroke and text:
            output_data[stroke] = f"{{^{text}^}}"

    # 2) 二文字以上助詞の規則生成（行 x 列）
    for row_id, column_ids in matrix.items():
        row = second_particles.get(row_id)
        if not row:
            continue

        row_text = row.get("text", "")
        row_stroke = row.get("stroke", "")
        if not row_text:
            continue

        for col_id in column_ids:
            col = first_particles.get(col_id)
            if not col:
                continue

            col_text = col.get("text", "")
            col_stroke = col.get("stroke", "")
            if not col_text:
                continue

            cell_key = f"{row_id}:{col_id}"
            text = overrides.get(cell_key, {}).get("text", f"{col_text}{row_text}")
            stroke = overrides.get(cell_key, {}).get("stroke", compose_stroke(col_stroke, row_stroke))

            if stroke and text:
                output_data[stroke] = f"{{^{text}^}}"

    # 3) 個別の追加入力（例外・臨時語）
    for entry in additional_entries:
        stroke = entry.get("stroke", "")
        text = entry.get("text", "")
        if stroke and text:
            output_data[stroke] = f"{{^{text}^}}"

    return output_data


if __name__ == "__main__":
    output_data = generate_particle_dictionary()
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "particle.json"))
    save_as_json(output_data, output_file_path)
    print(f"Generated data to {output_file_path}")
