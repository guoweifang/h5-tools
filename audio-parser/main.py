import os
import sys

# 定義 AudioFile 類別
class AudioFile:
    def __init__(self, file_path, relative_path):
        self.file_path = file_path
        self.relative_path = relative_path
        self.file_name_no_ext = os.path.splitext(os.path.basename(relative_path))[0]  # 去除副檔名的檔案名稱
        self.group = os.path.dirname(relative_path).split(os.sep)[-1]  # 取得資料夾名稱作為群組
        self.relative_dir = os.path.dirname(relative_path)

# 收集指定副檔名的檔案
def collect_files(folder_path, extension):
    files = []
    for root, dirs, file_names in os.walk(folder_path):
        for file_name in file_names:
            if file_name.endswith(extension):  # 檢查副檔名
                file_path = os.path.join(root, file_name)  # 完整檔案路徑
                relative_path = os.path.relpath(file_path, folder_path).replace("\\", "/")  # 相對路徑，跨平台兼容
                file = AudioFile(file_path, relative_path)
                files.append(file)
    return files

# 將檔案列表轉換成 TypeScript 的 enum 與設定格式並回傳字串
def generate_typescript(loader_name, files):
    # 生成 AudioKeys enum
    enum_lines = ["export enum AudioKeys {"]
    settings_lines = ["export const audioSettings: IAudioSetting[] = ["]

    for audio_file in files:
        # 取得音檔名稱，並轉換為鍵
        enum_key = audio_file.file_name_no_ext  # 使用去除副檔名的名稱
        relative_path = audio_file.relative_dir + '/' + audio_file.file_name_no_ext  # 不要副檔名
        group = audio_file.group

        # 添加到 enum 的行
        enum_lines.append(f"    {enum_key} = '{relative_path}',")

        # 添加到 audioSettings 的行
        settings_lines.append(f"    {{ loaderName: '{loader_name}', path: AudioKeys.{enum_key}, group: '{group}' }},")

    enum_lines.append("}\n")
    settings_lines.append("];\n")

    # 合併 enum 和設定，並回傳字串
    return "\n".join(enum_lines) + "\n" + "\n".join(settings_lines)

def main():
    # 檢查是否有提供資料夾路徑參數
    if len(sys.argv) < 2:
        print("請提供資料夾路徑")
        sys.exit(1)

    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"{folder_path} 不是有效的資料夾路徑")
        sys.exit(1)

    # 這裡設定要查找的副檔名，例如 ".txt"
    extension = ".mp3"

    loader_name = os.path.basename(folder_path)
    # 查找檔案
    audio_files = collect_files(folder_path, extension)

    # 列出結果
    if audio_files:
        # 生成 TypeScript 字串
        typescript_content = generate_typescript(loader_name, audio_files)

        # 顯示結果或進行後續處理
        print(typescript_content)

        # 將結果寫入檔案
        output_file_path = f"{loader_name}.ts"
        with open(output_file_path, "w") as f:
            f.write(typescript_content)
    else:
        print(f"沒有找到副檔名為 {extension} 的檔案。")

if __name__ == "__main__":
    main()