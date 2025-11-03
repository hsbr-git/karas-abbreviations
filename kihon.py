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

    output_data = {}

    consonant_list = {
        '':['a','i','u','e','o','ya','yu','yo'],
        'R': ['ka', 'ki', 'ku', 'ke', 'ko', 'kya', 'kyu', 'kyo'],
        'W': ['ta', 'ti', 'tu', 'te', 'to', 'tya', 'tyu', 'tyo'],
        'K': ['na', 'ni', 'nu', 'ne', 'no', 'nya', 'nyu', 'nyo'],
        'S': ['sa', 'si', 'su', 'se', 'so', 'sya', 'syu', 'syo'],
        'SK': ['ha', 'hi', 'hu', 'he', 'ho', 'hya', 'hyu', 'hyo'],
        'KW': ['ma', 'mi', 'mu', 'me', 'mo', 'mya', 'myu', 'myo'],
        'WR': ['ra', 'ri', 'ru', 're', 'ro', 'rya', 'ryu', 'ryo'],
        'SKW': ['ga', 'gi', 'gu', 'ge', 'go', 'gya', 'gyu', 'gyo'],
        'KWR': ['za', 'zi', 'zu', 'ze', 'zo', 'zya', 'zyu', 'zyo'],
        'KR': ['da', 'di', 'du', 'de', 'do', 'dya', 'dyu', 'dyo'],
        'SKR': ['wa', 'wi', 'vu', 'we', 'wo', 'va', 'vu', 'who'],
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

    # consonant_list と vowel_list を組み合わせて全パターンの辞書を生成
    # forループを使って、それぞれのリストの組み合わせを一つずつ処理します。
    for c_key, romaji_list in consonant_list.items():
        for v_key, index in vowel_list.items():
            # 新しいキーを作成します。
            # 子音キー(c_key)が空文字の場合は、母音キー(v_key)だけをキーにします。
            # それ以外は "子音キー-母音キー" という形式にします。
            if c_key == '':
                new_key = v_key
            else:
                new_key = f"{c_key}-{v_key}"
            
            # 作成したキーに、対応するローマ字を値として代入します。
            output_data[new_key] = romaji_list[index]

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
