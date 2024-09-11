from pydub import AudioSegment

# 載入音頻文件
audio = AudioSegment.from_file("./src/微積分 2024-09-09.m4a", format="m4a")

# 將音頻文件轉換為 WAV 格式
audio.export("./src/微積分 2024-09-09.wav", format="wav")

# 載入轉換後的 WAV 文件
audio = AudioSegment.from_file("./src/微積分 2024-09-09.wav", format="wav")

# 確定音頻的總長度（毫秒）
duration = len(audio)

# 計算切割點（音頻的一半）
halfway_point = duration // 2

# 切割音頻
first_half = audio[:halfway_point]
second_half = audio[halfway_point:]

# 將切割後的音頻保存為新文件
first_half.export("./src/微積分 2024-09-09 1.wav", format="wav")
second_half.export("./src/微積分 2024-09-09 2.wav", format="wav")
