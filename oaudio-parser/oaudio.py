import os
import sys
import audio_utils

def main(source_folder, temp_folder, output_folder, config_path, num_groups=6):
    print("流程開始...")

    # 取得來源資料夾名稱
    project_name = os.path.basename(os.path.normpath(source_folder))
    
    # 檢查來源資料夾
    if not audio_utils.check_source_folder(source_folder):
        print("錯誤: 來源資料夾不存在")
        return
    
    # 篩選音效資源
    audio_files = audio_utils.filter_audio_files(source_folder)
    if not audio_files:
        print("錯誤: 找不到音效檔案")
        return
    print(f"找到 {len(audio_files)} 個音效檔案")

    # 音效分組
    groups = audio_utils.group_audio_files(audio_files, num_groups)
    print("音效分組完成")

    # 生成合併音效檔案產出路徑 [{project_name}_{index}.mp3]
    os.makedirs(output_folder, exist_ok=True)
    output_audio_paths = []
    for i, group in enumerate(groups):
        output_audio_path = os.path.join(output_folder, f"{project_name}_{i}.mp3")
        output_audio_paths.append(output_audio_path)

    # 生成分組音效檔案
    audio_utils.generate_grouped_audio_files(groups, output_audio_paths, temp_folder)
    print("已生成分組音效檔案")

    # 生成音效設定檔
    audio_utils.generate_audio_settings(groups, output_audio_paths, config_path)
    print("音效設定檔已產出")
    
    # 清理暫存資料夾
    audio_utils.cleanup_temp_folder(temp_folder)
    print("清理暫存檔案")
    
    print("流程結束")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式: python main.py <來源資料夾>")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    temp_folder = './~temp'
    output_folder = './output'
    config_path = './audio_config.ts'
    
    main(source_folder, temp_folder, output_folder, config_path)
