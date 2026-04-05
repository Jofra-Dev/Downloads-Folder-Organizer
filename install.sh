#!/bin/bash

set -e

echo "====================================="
echo "File Organizer Installation Script"
echo "====================================="
echo ""

if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use: sudo ./install.sh)"
    exit 1
fi

echo "✅ Running as root"

APP_USER="${SUDO_USER:-$USER}"
APP_DIR="/opt/file-organizer"
LOG_DIR="/var/log/file-organizer"
CONFIG_DIR="/etc/file-organizer"

echo ""
echo "📁 Creating directories..."
mkdir -p "$APP_DIR" "$LOG_DIR" "$CONFIG_DIR"
echo "✅ Directories created"

echo ""
echo "📄 Copying application files..."

if ls *.py 1> /dev/null 2>&1; then
    cp *.py "$APP_DIR/"
    echo "✅ Python files copied"
else
    echo "❌ No .py files found"
    exit 1
fi

if ls *.json 1> /dev/null 2>&1; then
    cp *.json "$CONFIG_DIR/"
    echo "✅ JSON files copied"
else
    echo "⚠️ Creating default config.json"
    cat > "$CONFIG_DIR/config.json" << 'EOF'
{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
  "Docs": [".pdf", ".docx", ".txt", ".md", ".csv"],
  "Videos": [".mp4", ".mkv", ".avi", ".mov"],
  "Audio": [".mp3", ".wav", ".flac"],
  "Archives": [".zip", ".tar", ".gz", ".rar"]
}
EOF
    echo "✅ Default config.json created"
fi

echo ""
echo "🔗 Creating symlink for config..."
ln -sf "$CONFIG_DIR/config.json" "$APP_DIR/config.json"
echo "✅ Symlink created"

echo ""
echo "🔐 Setting permissions..."
chown -R "$APP_USER:$APP_USER" "$APP_DIR" "$LOG_DIR" "$CONFIG_DIR"
echo "✅ Permissions set"

echo ""
echo "🚀 Making main.py executable..."
chmod +x "$APP_DIR/main.py"
echo "✅ main.py is executable"

echo ""
echo "🐍 Setting up Python virtual environment..."
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null
pip install watchdog > /dev/null
deactivate
echo "✅ Virtual environment created"

echo ""
echo "====================================="
echo "✅ INSTALLATION COMPLETE!"
echo "====================================="
echo ""
echo "Next steps:"
echo "  sudo nano /etc/systemd/system/file-organizer.service"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable file-organizer"
echo "  sudo systemctl start file-organizer"
echo "  sudo systemctl status file-organizer"
echo ""
echo "====================================="