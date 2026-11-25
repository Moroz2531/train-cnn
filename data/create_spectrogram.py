import os
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')  # Чтобы скрипт не падал на сервере без монитора
import matplotlib.pyplot as plt

def create_spectrogram(audio_file, image_file):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    
    y, sr = librosa.load(audio_file)
    ms = librosa.feature.melspectrogram(y=y, sr=sr)
    log_ms = librosa.power_to_db(ms, ref=np.max)
    librosa.display.specshow(log_ms, sr=sr)
    
    fig.savefig(image_file)
    plt.close(fig)

def create_pngs_from_wavs(input_path, output_path):
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.wav'):
                input_file = os.path.join(root, file)
                
                # Вычисляем относительный путь, чтобы повторить структуру подпапок
                rel_dir = os.path.relpath(root, input_path)
                target_dir = os.path.join(output_path, rel_dir)
                
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                # Меняем расширение безопасно (работает и для .wav, и для .WAV)
                base_name = os.path.splitext(file)[0]
                output_file = os.path.join(target_dir, f"{base_name}.png")
                
                create_spectrogram(input_file, output_file)
                print(f"Готово: {output_file}")

# Указываем путь относительно расположения самого скрипта, чтобы не было FileNotFoundError
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(BASE_DIR, 'voice-data-minist')
output_folder = os.path.join(BASE_DIR, 'spectrograms', 'voice-data-minist')

create_pngs_from_wavs(input_folder, output_folder)
