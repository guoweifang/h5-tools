import os
import shutil
import json
import subprocess
from pydub import AudioSegment
import shlex

def check_source_folder(source_folder: str):
    """檢查來源資料夾是否存在，若不存在則返回 False"""
    return os.path.exists(source_folder) and os.path.isdir(source_folder)

def filter_audio_files(source_folder: str, extension=".mp3"):
    """篩選來源資料夾內的音效資源 (包含子資料夾，僅限指定格式)"""
    audio_files = []
    for root, _, files in os.walk(source_folder):
        audio_files.extend(os.path.join(root, f) for f in files if f.endswith(extension))

    # 印出音效檔案清單
    for i, file in enumerate(audio_files):
        print(f"{i + 1}. {file}")
    return audio_files

def compress_audio_file(audio_file: str, temp_folder: str):
    """壓縮音效檔案並存入暫存資料夾，避免影響原始檔案"""
    os.makedirs(temp_folder, exist_ok=True)
    temp_file_name = "~" + os.path.basename(audio_file)
    output_path = os.path.join(temp_folder, temp_file_name)
    arguments = f"-i \"{audio_file}\" -c:a libmp3lame -ar 44100 -ac 2 -q:a 8 -y \"{output_path}\""
    print(f"壓縮音效檔案: {audio_file} -> {output_path}")
    subprocess.run(['ffmpeg'] + shlex.split(arguments), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

def cleanup_temp_folder(temp_folder: str):
    """刪除暫存資料夾"""
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

def group_audio_files(audio_files: list, num_groups: int):
    """根據音效時間長度進行分組，使各組時間長度盡量均衡"""
    groups = [[] for _ in range(num_groups)]
    group_durations = [0] * num_groups
    
    for file in audio_files:
        duration = AudioSegment.from_file(file).duration_seconds
        min_index = group_durations.index(min(group_durations))
        offset = group_durations[min_index]
        # category: 父資料夾名稱
        category = os.path.basename(os.path.dirname(file))
        group_durations[min_index] += duration
        groups[min_index].append({
            "file": file,
            "group": min_index,
            "offset": offset,
            "duration": duration,
            "category": category
        })

    return groups

def generate_audio_settings(groups: list, merged_file_paths: list, output_path: str):
    """生成 TypeScript 音效設定檔"""
    # no extension
    merged_file_names = {i: os.path.basename(f).replace(".mp3", "") for i, f in enumerate(merged_file_paths)}

    audio_keys = {}
    audio_settings = {}
    for group in groups:
        for item in group:
            file = item["file"]
            # 從檔案名稱生成typescript的enum key
            key = os.path.basename(file).replace(".mp3", "").replace(" ", "_").upper()
            audio_keys[key] = key

            group_index = item["group"]
            category = item["category"]
            begin = item["offset"]
            duration = item["duration"]

            audio_settings[key] = {
                "key": key,
                "group": merged_file_names[group_index],
                "category": category,
                "begin": begin,
                "duration": duration
            }
    
    ts_content = f"""
export enum AudioKeys {{
    {',\n\t'.join(f'{key} = "{value}"' for key, value in audio_keys.items())}
}}

export const groupFiles: string[] = [
    {',\n\t'.join(f'"{value}"' for _, value in merged_file_names.items())}
];

export const audioSettings: Record<AudioKeys, {{
    key: string;
    group: string;
    category: string;
    begin: number;
    duration: number;
}}> = {json.dumps(audio_settings, indent=4)};
    """
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ts_content)

def generate_grouped_audio_files(groups: list, output_audio_paths: list, temp_folder: str):
    """生成分組後的音效檔案"""

    # 依照groups數量生成分組音效檔案AudioSegment.empty()
    audio_segments = [AudioSegment.empty() for _ in range(len(groups))]

    for _, group in enumerate(groups):
        for item in group:
            file = item["file"]
            group_index = item["group"]

            # 建立壓縮後的檔案
            compressed_file = compress_audio_file(file, temp_folder)
            audio_segments[group_index] += AudioSegment.from_file(compressed_file)

    for i, segment in enumerate(audio_segments):
        output_path = output_audio_paths[i]
        segment.export(output_path, format="mp3")