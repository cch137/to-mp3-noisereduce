import noisereduce as nr
import os
import pydub
import numpy as np
import io

# 確認是否為音頻文件
def is_audio_file(file_path):
    audio_extensions = ('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')
    return file_path.lower().endswith(audio_extensions)

# 處理音頻，進行降噪並輸出到指定路徑
def produce_audio(input_filepath, output_filepath):
    input_filepath = os.path.abspath(input_filepath)

    # 讀取音頻文件
    audio1 = pydub.AudioSegment.from_file(input_filepath)

    # 將音頻轉換為 WAV 格式的數據，並使用 BytesIO 進行內存處理
    wav_buffer = io.BytesIO()
    audio1.export(wav_buffer, format="wav")
    wav_buffer.seek(0)
    
    # 讀取 WAV 數據並進行噪聲降低
    audio1 = pydub.AudioSegment.from_wav(wav_buffer)
    audio_array = np.array(audio1.get_array_of_samples())

    # 降噪處理
    prop_decrease = 4 / 5
    reduced_noise = nr.reduce_noise(y=audio_array, sr=audio1.frame_rate, prop_decrease=prop_decrease)

    # 將處理後的音頻數據轉換回 AudioSegment
    reduced_audio = pydub.AudioSegment(
        reduced_noise.astype(np.int16).tobytes(),
        frame_rate=audio1.frame_rate,
        sample_width=audio1.sample_width,
        channels=audio1.channels
    )

    # 將處理後的音頻直接輸出為 MP3 文件
    with io.BytesIO() as mp3_buffer:
        reduced_audio.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)
        with open(output_filepath, "wb") as f:
            f.write(mp3_buffer.read())

if __name__ == "__main__":
    # 設定來源和輸出目錄
    input_directory = os.path.abspath("./src/")
    output_directory = os.path.abspath("./assets/")
    
    # 確保輸出資料夾存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Source folder path
    source_folder = './src/'

    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        
        # Ensure it's a file, not a directory
        if os.path.isfile(file_path):
            # Check file extension
            if not filename.lower().endswith('.mp3'):
                try:
                    # Load the audio file
                    audio = pydub.AudioSegment.from_file(file_path)
                    
                    # Determine new file name
                    new_filename = os.path.splitext(filename)[0] + '.mp3'
                    new_file_path = os.path.join(source_folder, new_filename)
                    
                    # Convert the audio file to MP3 format
                    audio.export(new_file_path, format="mp3")
                    
                    # Delete the original file
                    os.remove(file_path)
                    print(f"Converted and deleted file: {filename}")
                
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
            else:
                print(f"Skipped file: {filename} (already in MP3 format)")

    # 遍歷來源資料夾中的文件
    filenames = os.listdir(input_directory)
    for filename in filenames:
        input_filepath = os.path.join(input_directory, filename)
        
        # 確認是音頻文件，且不是 MP3 格式
        if os.path.isfile(input_filepath) and is_audio_file(input_filepath):
            output_filepath = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.mp3")
            
            # 如果輸出文件不存在，則進行處理
            if not os.path.exists(output_filepath):
                print("Processing:", input_filepath)
                produce_audio(input_filepath, output_filepath)

print("DONE")
input("Press Enter to exit...")
