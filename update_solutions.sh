#!/bin/bash

# Сперва сохраняет изменения в текущей ветке,
# -затем переход в main-ветку, 
# -получение изменений с удаленного репозитория,
# -полное обновление мастер-ветки,
# -копирование этих изменнеий смастер в текущую ветку,
# -сохранение этих изменений в текущей ветке.

set -e

# Проверка наличия не внесенных в индекс или незакоммиченных изменений
# Если такие имеются, то произвести автокоммит

if ! git diff --quiet || ! git diff --cached --quiet
then
    echo "Есть незакоммиченные изменения"

    git add .
    git commit -m "Auto commit before update"
else
    echo "Изменений нет"
fi

echo "Переход в master..."
git checkout main

echo "Получение изменений..."
git fetch origin

echo "Полное обновление master..."
git reset --hard origin/main

echo "Переход в solutions..."
git checkout solutions

echo "Копирование новых файлов и изменений из master..."
git checkout main -- .

echo "Добавляем в индекс и коммитим новые изменения в ветке solutions..."
git add .
git commit -m "Автомат"

echo "ГОТОВО! Молодец!"
