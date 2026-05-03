### Install a script with dependencies
```bash
git clone https://github.com/boradydev/log_bridge && \
cd log_bridge

sudo apt install software-properties-common && \
sudo add-apt-repository ppa:deadsnakes/ppa && \
sudo apt install python3.13 python3.13-venv python3.13-dev

python3.13 -m venv .venv && \
source .venv/bin/activate && \
pip install poetry && \
poetry install
```
### Manual run for checking
```bash
.venv/bin/python -m src.main
```
### Systemd service file for auto run the bot
```bash
sudo nano /etc/systemd/system/log-bridge.service
```
```text
[Unit]
Description=Log Bridge Telegram Bot
After=network.target

[Service]
User=bestuser
Group=bestuser
WorkingDirectory=/home/bestuser/log_bridge
EnvironmentFile=/home/bestuser/log_bridge/.env
ExecStart=/home/bestuser/log_bridge/.venv/bin/python -m src.main

StandardOutput=append:/home/bestuser/log_bridge/bot_output.log
StandardError=inherit

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload && \
sudo systemctl enable log-bridge.service && \
sudo systemctl start log-bridge.service
```
### Check the bot output
```bash
tail bot_output.log
```
### Project git update in the project folder (inner the log_bridge folder)
```bash
git pull origin master
```
### Add a user to the adm group (recommended)
```bash
sudo usermod -aG adm $USER && \
newgrp adm
```
### Set permissions for the log file (if needed, not recommended)
```bash
sudo chmod 644 /var/log/some_log_file.log
```