#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# install.sh — TikTok Checker setup
# Funciona em: Termux (Android), Linux, macOS
# ─────────────────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GRN}[OK]${NC} $1"; }
warn() { echo -e "${YLW}[..] $1${NC}"; }
err()  { echo -e "${RED}[ERRO] $1${NC}"; }

echo ""
echo -e "${RED}  TikTok Checker — Instalacao${NC}"
echo "  ─────────────────────────────"
echo ""

# ── Detectar ambiente ─────────────────────────────────────────────────────────
IS_TERMUX=false
IS_LINUX=false
IS_MAC=false

if [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
    warn "Ambiente detectado: Termux (Android)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    IS_MAC=true
    warn "Ambiente detectado: macOS"
else
    IS_LINUX=true
    warn "Ambiente detectado: Linux"
fi

echo ""

# ── Termux: instalar pkg deps ─────────────────────────────────────────────────
if [ "$IS_TERMUX" = true ]; then
    warn "Atualizando pacotes Termux..."
    pkg update -y 2>/dev/null
    
    warn "Instalando Python..."
    pkg install python -y 2>/dev/null && ok "python" || err "python falhou"

    warn "Instalando chafa (visualizacao de imagem)..."
    pkg install chafa -y 2>/dev/null && ok "chafa" || warn "chafa nao disponivel — ok, continuando"

    warn "Instalando openssl..."
    pkg install openssl -y 2>/dev/null && ok "openssl" || warn "openssl falhou"

    warn "Instalando libffi..."
    pkg install libffi -y 2>/dev/null && ok "libffi" || true

fi

# ── Linux: verificar/instalar deps de sistema ─────────────────────────────────
if [ "$IS_LINUX" = true ]; then
    if command -v apt-get &>/dev/null; then
        warn "Instalando dependencias do sistema..."
        apt-get install -y python3 python3-pip libssl-dev 2>/dev/null && ok "apt deps" || true
        apt-get install -y chafa 2>/dev/null && ok "chafa" || warn "chafa nao disponivel"
    elif command -v pacman &>/dev/null; then
        pacman -S --noconfirm python python-pip chafa 2>/dev/null && ok "pacman deps" || true
    fi
fi

# ── macOS: verificar/instalar deps ───────────────────────────────────────────
if [ "$IS_MAC" = true ]; then
    if command -v brew &>/dev/null; then
        brew install chafa 2>/dev/null && ok "chafa" || warn "chafa nao disponivel"
    fi
fi

# ── pip install ───────────────────────────────────────────────────────────────
echo ""
warn "Instalando dependencias Python..."

# Tentar pip normal primeiro, depois com flags para Termux/sistema
PIP_CMD=""
if command -v pip3 &>/dev/null; then
    PIP_CMD="pip3"
elif command -v pip &>/dev/null; then
    PIP_CMD="pip"
elif command -v python3 &>/dev/null; then
    PIP_CMD="python3 -m pip"
elif command -v python &>/dev/null; then
    PIP_CMD="python -m pip"
fi

if [ -z "$PIP_CMD" ]; then
    err "pip nao encontrado. Instale Python manualmente."
    exit 1
fi

# Instalar com --break-system-packages para evitar erro no Termux/Linux novo
install_pkg() {
    PKG=$1
    warn "Instalando $PKG..."
    $PIP_CMD install "$PKG" --break-system-packages -q 2>/dev/null \
    || $PIP_CMD install "$PKG" -q 2>/dev/null \
    || $PIP_CMD install "$PKG" --user -q 2>/dev/null
    
    if [ $? -eq 0 ]; then
        ok "$PKG"
    else
        err "$PKG falhou — tente manualmente: $PIP_CMD install $PKG"
    fi
}

install_pkg requests
install_pkg colorama
install_pkg urllib3
install_pkg PySocks

echo ""
ok "Instalacao concluida!"
echo ""
echo -e "  Para rodar: ${GRN}python tiktok_checker.py${NC}"
echo -e "  Imagem:     Coloque ${YLW}msk.jpg${NC} na mesma pasta que a script ( voce pode escolher uma imagem personalizada.)"
echo ""
