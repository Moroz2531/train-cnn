#!/bin/bash

# Корневая папка со спектрограммами и подпапками
TARGET_DIR="/home/admin/graduate-work/first/spectrograms/voice-data-minist"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Ошибка: папка $TARGET_DIR не найдена."
    exit 1
fi

# Ищем все .png файлы во всех поддиректориях, начинающиеся с цифры 0-9
find "$TARGET_DIR" -type f -name "[0-9]*.png" | while read -r filepath; do
    # Получаем только имя файла без пути (например, 3_george_12.png)
    filename=$(basename "$filepath")
    
    # Извлекаем первую цифру
    digit="${filename:0:1}"
    
    # Папка назначения в корне TARGET_DIR (например, .../voice-data-minist/3)
    dest_dir="$TARGET_DIR/$digit"
    
    # Пропускаем, если файл уже лежит в нужной папке
    if [ "$(dirname "$filepath")" == "$dest_dir" ]; then
        continue
    fi
    
    mkdir -p "$dest_dir"
    mv "$filepath" "$dest_dir/"
    echo "Перемещён: $filepath -> $dest_dir/$filename"
done

echo "Рекурсивная сортировка завершена!"
