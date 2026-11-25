#!/usr/bin/env bash
#
# Скрипт создания виртуального окружения и установки зависимостей
# для проекта graduate-work (Keras / TensorFlow).
#
# Использование:
#   chmod +x setup_env.sh
#   ./setup_env.sh
#
set -euo pipefail

# -------------------- настройки --------------------
VENV_DIR="venv"
PYTHON_BIN="python3"

# Пакеты, которые должны быть в окружении.
# tensorflow уже включает keras и numpy, но перечисляем явно для наглядности.
REQUIRED_PACKAGES=(
    "tensorflow"
    "keras"
    "matplotlib"
    "pillow"
    "numpy"
)

# -------------------- утилиты --------------------
log()  { printf '\033[1;34m[INFO]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[WARN]\033[0m %s\n' "$*"; }
err()  { printf '\033[1;31m[ERR ]\033[0m %s\n' "$*" >&2; }

need_sudo() {
    if [[ $EUID -ne 0 ]]; then
        echo sudo
    else
        echo ""
    fi
}

# -------------------- 1. проверка python3 --------------------
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    err "Не найден $PYTHON_BIN. Установите Python 3 и повторите."
    exit 1
fi
log "Найден $($PYTHON_BIN --version)"

# -------------------- 2. проверка/установка python3-venv и python3-pip --------------------
SUDO="$(need_sudo)"
VENV_OK=1
"$PYTHON_BIN" -c "import venv" 2>/dev/null || VENV_OK=0

if [[ $VENV_OK -eq 0 ]]; then
    warn "Модуль venv не найден — пробую установить python3-venv / python3-pip через apt."
    if command -v apt >/dev/null 2>&1; then
        $SUDO apt update
        $SUDO apt install -y python3-venv python3-pip python3-full
    else
        err "apt недоступен. Установите python3-venv вручную и повторите."
        exit 1
    fi
fi

# -------------------- 3. создание виртуального окружения --------------------
if [[ -d "$VENV_DIR" && -f "$VENV_DIR/bin/activate" ]]; then
    log "Виртуальное окружение '$VENV_DIR' уже существует — переиспользую."
else
    log "Создаю виртуальное окружение в '$VENV_DIR'..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# -------------------- 4. активация --------------------
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
log "Активно окружение: $(which python) ($(python --version 2>&1))"

# -------------------- 5. обновление pip / setuptools / wheel --------------------
log "Обновляю pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

# -------------------- 6. установка недостающих пакетов --------------------
log "Проверяю наличие пакетов..."
MISSING=()
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    # Имена модулей для импорта могут отличаться от имён пакетов
    case "$pkg" in
        pillow) import_name="PIL" ;;
        *)      import_name="$pkg" ;;
    esac
    if python -c "import ${import_name}" 2>/dev/null; then
        log "  ✓ $pkg уже установлен"
    else
        warn "  ✗ $pkg отсутствует — будет установлен"
        MISSING+=("$pkg")
    fi
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
    log "Устанавливаю: ${MISSING[*]}"
    python -m pip install "${MISSING[@]}"
else
    log "Все пакеты уже установлены — установка не требуется."
fi

# -------------------- 7. проверка версий --------------------
log "Версии установленных библиотек:"
python - <<'PY'
import importlib
for name in ("tensorflow", "keras", "numpy", "matplotlib", "PIL"):
    try:
        m = importlib.import_module(name)
        ver = getattr(m, "__version__", "?")
        print(f"  {name:12s} {ver}")
    except Exception as e:
        print(f"  {name:12s} ОШИБКА: {e}")
PY

# -------------------- 8. подсказка --------------------
cat <<EOF

✅ Готово. Окружение '$VENV_DIR' настроено.

Чтобы начать работу, выполните в текущем терминале:
    source $VENV_DIR/bin/activate

Затем можно запускать ваш скрипт:
    python your_script.py

Выйти из окружения:
    deactivate

EOF
