# Downloads Folder Organizer

## Overview

An automated Linux service that organizes your Downloads folder by
moving files into categorized subfolders based on their extensions.

## Features

-   Real-time monitoring: Automatically detects new files
-   Smart organization: Moves files into folders like Images, Docs,
    Videos, etc.
-   Smart delay: Waits for downloads to complete before moving
-   Duplicate prevention: Automatically renames conflicting files
-   systemd service: Runs in the background and starts with the system
-   Full logging: Records all operations for debugging
-   Configurable: Easily add/remove extensions and categories

## Default Categories

  -----------------------------------------------------------------------
  Category                          Extensions
  --------------------------------- -------------------------------------
  Images                            .jpg, .jpeg, .png, .gif, .bmp, .svg,
                                    .webp

  Docs                              .pdf, .docx, .doc, .txt, .md, .rtf,
                                    .odt, .xlsx, .xls, .pptx, .csv

  Videos                            .mp4, .mkv, .avi, .mov, .wmv, .flv,
                                    .webm

  Audio                             .mp3, .wav, .flac, .aac, .ogg, .m4a

  Archives                          .zip, .tar, .gz, .rar, .7z, .bz2, .xz

  Programming                       .py, .js, .html, .css, .java, .cpp,
                                    .c, .json, .xml

  Executables                       .exe, .msi, .deb, .rpm, .sh, .bin

  Others                            Any unlisted extension
  -----------------------------------------------------------------------

## Requirements

-   Linux (Ubuntu/Debian recommended)
-   Python 3.8+
-   pip3
-   systemd

## Quick Installation

``` bash
git clone https://github.com/Jofra-Dev/Downloads-Folder-Organizer.git
cd downloads-organizer
sudo ./install.sh

sudo nano /etc/systemd/system/file-organizer.service

sudo systemctl daemon-reload
sudo systemctl enable file-organizer
sudo systemctl start file-organizer
```

## Manual Installation

### Install dependencies

``` bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
pip install watchdog
```

### Setup virtual environment

``` bash
python3 -m venv venv
source venv/bin/activate
pip install watchdog
deactivate
```

### Test manually

``` bash
python main.py --path ~/Downloads --log-level DEBUG
```

### Install as service

``` bash
sudo mkdir -p /opt/file-organizer
sudo cp *.py /opt/file-organizer/
sudo cp *.json /etc/file-organizer/
sudo ln -sf /etc/file-organizer/config.json /opt/file-organizer/config.json
```

## Configuration

Edit the configuration file:

``` bash
sudo nano /etc/file-organizer/config.json
```

Example:

``` json
{
  "Images": [".jpg", ".png", ".gif"],
  "Documents": [".pdf", ".docx", ".txt"],
  "Projects": [".py", ".js", ".html"],
  "Media": [".mp4", ".mp3"]
}
```

Restart service:

``` bash
sudo systemctl restart file-organizer
```

## Useful Commands

### Manage service

``` bash
sudo systemctl start file-organizer
sudo systemctl stop file-organizer
sudo systemctl restart file-organizer
sudo systemctl status file-organizer
```

### Logs

``` bash
sudo journalctl -u file-organizer -f
sudo tail -f /var/log/file-organizer/app.log
```

### Debug mode

``` bash
cd /opt/file-organizer
source venv/bin/activate
python main.py --log-level DEBUG --path ~/Downloads
```

## Uninstall

``` bash
sudo systemctl stop file-organizer
sudo systemctl disable file-organizer
sudo rm /etc/systemd/system/file-organizer.service

sudo rm -rf /opt/file-organizer
sudo rm -rf /var/log/file-organizer
sudo rm -rf /etc/file-organizer

sudo systemctl daemon-reload
```

## Troubleshooting

### Service not starting

``` bash
sudo journalctl -u file-organizer -n 50
ls -la ~/Downloads/
```

### Files not moving

``` bash
cat /etc/file-organizer/config.json
```

### Permission issues

``` bash
sudo chown -R $USER:$USER /opt/file-organizer
sudo chown -R $USER:$USER /var/log/file-organizer
```

## Project Structure

    downloads-organizer/
    ├── main.py
    ├── watcher.py
    ├── classifier.py
    ├── move.py
    ├── scanner.py
    ├── config.py
    ├── config.json
    ├── install.sh
    └── README.md

## Contributing

-   Fork the project
-   Create your branch
-   Commit your changes
-   Push and open a Pull Request

## License

MIT License

## Warning

This service automatically moves files. It is recommended to: - Backup
important files - Test with a sample folder first - Review configuration
before production use