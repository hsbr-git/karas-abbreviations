import json
import os

def create_data():
    """
    JSONに変換したいPythonのデータ構造（辞書やリスト）を作成する関数。
    ここに独自のルールを記述していきます。
    
    Returns:
        dict or list: JSONに変換するデータ
    """
    # --- ここからルールを記述 ---

    output_data = {
        '*E': '{^nn^}',  # ん
        '*U': '{^ltu^}', # っ
        '*EU': '{^-^}',  # ー
    }

    consonant_list = {
        '':['a','i','u','e','o','ya','yu','yo'],
        'S': ['sa', 'si', 'su', 'se', 'so', 'sya', 'syu', 'syo'],
        'K': ['ta', 'ti', 'tu', 'te', 'to', 'tya', 'tyu', 'tyo'],
        'W': ['na', 'ni', 'nu', 'ne', 'no', 'nya', 'nyu', 'nyo'],
        'R': ['ka', 'ki', 'ku', 'ke', 'ko', 'kya', 'kyu', 'kyo'],
        'SK': ['ha', 'hi', 'hu', 'he', 'ho', 'hya', 'hyu', 'hyo'],
        'KW': ['ma', 'mi', 'mu', 'me', 'mo', 'mya', 'myu', 'myo'],
        'WR': ['ra', 'ri', 'ru', 're', 'ro', 'rya', 'ryu', 'ryo'],
        'SKW': ['za', 'zi', 'zu', 'ze', 'zo', 'zya', 'zyu', 'zyo'],
        'KWR': ['ga', 'gi', 'gu', 'ge', 'go', 'gya', 'gyu', 'gyo'],
        'KR': ['da', 'di', 'du', 'de', 'do', 'dya', 'dyu', 'dyo'],
        'SKR': ['wa', 'wi', 'nn', 'we', 'wo', 'va', 'vu', 'who'],
        'SR': ['ba', 'bi', 'bu', 'be', 'bo', 'bya', 'byu', 'byo'],
        'SW': ['pa', 'pi', 'pu', 'pe', 'po', 'pya', 'pyu', 'pyo'],
        'SWR': ['la', 'li', 'lu', 'le', 'lo', 'lya', 'lyu', 'lyo'],
    }

    vowel_list={
        'R': 0,   # あ
        'B': 1,   # い
        'RG': 2,  # う
        'S': 3,   # え
        'G': 4,   # お
        'RB': 5,  # や
        'RBG': 6, # ゆ
        'BG': 7,  # よ
    }

    # 親指キーの左右の割り当て
    left_thumb_keys = ['A', 'O']
    right_thumb_keys = ['E', 'U']    

    # 親指キーによるショートカットの定義
    # キー: 追加されるローマ字（基本）
    shortcut_list = {
        'A': 'ku',  # く
        'O': 'u',   # う
        'E': 'nn',   # ん
        'U': 'ltu', # っ (Ploverで「っ」を入力するための一般的なローマ字)
        'AO': 'tsu',# つ
        'EU': '-',  # ー (長音)
    }

    # consonant_list と vowel_list を組み合わせて全パターンの辞書を生成
    # forループを使って、それぞれのリストの組み合わせを一つずつ処理します。
    for c_key, romaji_list in consonant_list.items():
        for v_key, index in vowel_list.items():
            # 新しいキーを作成します。
            # 左手キー(c_key)と右手キー(v_key)をハイフンで結合
            new_key = f"{c_key}-{v_key}"
            
            # 対応するローマ字をPlover形式に変換し、作成したキーに値として代入します。
            base_romaji = romaji_list[index]
            output_data[new_key] = f"{{^{base_romaji}^}}"

            # --- ショートカットパターンの追加 ---
            # 基本モーラにショートカットキーを組み合わせたパターンを生成します。
            for s_key, s_romaji in shortcut_list.items():
                # --- 「い段」「え段」の特別ルール ---
                # 不規則リストに基づいてショートカットの内容を変更
                temp_s_romaji = s_romaji
                if s_key == 'O': # 「う」のショートカット
                    if base_romaji.endswith('a'): # 「あ段＋う」→「あ段＋い」
                        temp_s_romaji = 'i'
                    elif base_romaji.endswith('i'): # 「い段＋う」→「い段＋い」
                        temp_s_romaji = 'i'
                    elif base_romaji.endswith('e'): # 「え段＋う」→「え段＋い」
                        temp_s_romaji = 'i'
                    elif base_romaji.endswith('ya'): # 「や段＋う」→「や段＋あ」
                        temp_s_romaji = 'a'
                elif s_key == 'A': # 「く」のショートカット
                    if base_romaji.endswith('i'): # 「い段＋く」→「い段＋き」
                        temp_s_romaji = 'ki'
                    elif base_romaji.endswith('e'): # 「え段＋く」→「え段＋き」
                        temp_s_romaji = 'ki'
                
                combined_romaji = base_romaji + temp_s_romaji
                
                # --- キーの左右振り分け ---
                left_consonant_keys = c_key
                left_thumb_part = ""
                right_thumb_part = ""
                right_vowel_keys = v_key

                # ショートカットキーの各文字をチェックして左右に振り分け
                for char in s_key:
                    if char in left_thumb_keys:
                        left_thumb_part += char
                    elif char in right_thumb_keys:
                        right_thumb_part += char
                    else: # RB, GSなどの場合
                        right_vowel_keys += char
                
                # 左右のキーを結合してショートカットキーを生成
                shortcut_key = f"{left_consonant_keys}{left_thumb_part}-{right_thumb_part}{right_vowel_keys}"
                if shortcut_key not in output_data: # 重複を避ける
                    output_data[shortcut_key] = f"{{^{combined_romaji}^}}"

    # --- ここまでルールを記述 ---
    return output_data

def save_as_json(data, file_path):
    """
    受け取ったデータを指定されたパスにJSONファイルとして保存する関数。

    Args:
        data (dict or list): 保存したいデータ。
        file_path (str): 保存先のファイルパス。
    """
    try:
        # ファイルの親ディレクトリが存在しない場合は作成する
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")

        # ファイルにデータを書き込む
        # 'w'モード: ファイルが存在すれば上書き、なければ新規作成
        # encoding='utf-8': 日本語などのマルチバイト文字を正しく扱うため
        with open(file_path, 'w', encoding='utf-8') as f:
            # json.dump() を使ってファイルに書き込む
            # indent=4: 人間が読みやすいようにインデントを付ける
            # ensure_ascii=False: 日本語をそのまま出力する（エスケープしない）
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Successfully saved JSON data to: {file_path}")

    except TypeError as e:
        print(f"❌ Error: データ型に問題があります。JSONに変換できないオブジェクトが含まれている可能性があります。 - {e}")
    except Exception as e:
        print(f"❌ An error occurred while saving the file: {e}")


# このスクリプトが直接実行されたときに以下の処理を行う
if __name__ == "__main__":
    # 1. ルールに基づいてデータを作成
    my_data = create_data()
    
    # 2. 保存するファイルパスを指定
    # 例: output/karas_main.json というファイル名で保存
    output_file_path = "output/karas_main.json"
    
    # 3. 作成したデータをJSONファイルとして保存
    save_as_json(my_data, output_file_path)
