# Log Monitoring System (aiogram-based)

This project is an event-driven log monitoring service built on top of the **aiogram** framework. It tracks log file updates in real-time and executes business logic based on detected patterns.

## Architecture Diagram

```text
                  ┌──────────────────────┐
                  │  aiogram.Dispatcher  │
                  │  (Main Lifecycle)    │
                  └──────────┬───────────┘
            ┌────────────────┴────────────────┐
            │                                 │ 
            ▼                                 ▼
    ┌───────────────┐                 ┌───────────────┐
    │  on_startup() │                 │ on_shutdown() │
    │  log file     │                 └───────────────┘
    │  dispatcher   │                 
    └───────┬───────┘ 
            │                                 
            ▼                                 
    ┌─────────────────────────────────────────────────┐
    │          Background Tasks (asyncio)             │
    └───────┬────────────────────────┬────────────────┘
            │                        │
            ▼                        ▼
    ┌─────────────────────┐        ┌─────────────────────┐
    │  Log Dispatcher 1   │        │  Log Dispatcher 2   │
    └─────────┬───────────┘        └─────────────────────┘
              │                        
            ┌─┴───────────────────────────┐
            │   list Routes (1:N)         │
            ▼                             ▼
    ┌───────────────┐                 ┌───────────────┐
    │    Route      │                 │    Route      │
    │ ───────────── │                 │ ───────────── │
    │ [ Regex/DTO ] │                 │ [ Regex/DTO ] │
    └───────┬───────┘                 └───────┬───────┘
            │                                 │
            ▼                                 ▼
    ┌───────────────┐                 ┌───────────────┐
    │    DTO        │                 │    DTO        │
    │ ───────────── │                 │ ───────────── │
    │ - Validation  │                 │ - Validation  │
    │ - Parsing     │                 │ - Parsing     │
    └─────────┬─────┘                 └───────────────┘
              │                        
            ┌─┴───────────────────────────┐
            │   list Cases (1:N)          │
            ▼                             ▼
    ┌───────────────┐                 ┌───────────────┐
    │    Case 1     │                 │    Case 2     │
    └───────────────┘                 └───────────────┘
```

## Technical Description

### 1. Lifecycle Management (aiogram)
The application leverages the `aiogram.Dispatcher` as its primary engine.
*   **Startup**: The framework initializes infrastructure components (LogFiles, Notifiers) and spawns asynchronous background tasks for each log stream.
*   **Shutdown**: Ensures a clean exit by closing file handles and terminating network sessions (Telegram API, etc.).

### 2. Log Dispatcher (Orchestrator)
The Dispatcher is the bridge between the physical file and the application logic.
*   **1:1 Binding**: Each Dispatcher is dedicated to one specific log file.
*   **Non-blocking I/O**: It monitors file updates using `asyncio`, ensuring high performance without blocking the bot's main loop.
*   **Distribution**: Raw lines are passed to a collection of registered Routes.

### 3. Routing & Validation (Route & DTO)
*   **Route**: Filters incoming log lines (e.g., via Regular Expressions) to determine which events should be handled.
*   **DTO (Data Transfer Object)**: Responsible for data integrity.
    *   **Parsing**: Converts unstructured text into structured Python objects.
    *   **Validation**: Acts as a gatekeeper, ensuring only valid and cleaned data reaches the use cases.

### 4. Business Logic (Cases)
*   **1:N Execution**: A single Route can trigger multiple **Cases** (actions).
*   **Decoupling**: Business logic is isolated from the log-parsing logic, allowing for easy testing and modification.
*   **Error Isolation**: Failure in one Case does not interrupt other Cases or the overall log-stream processing.

## Why This Architecture?
- **Scalability**: Add new log monitors by simply registering a new Dispatcher.
- **Maintainability**: Clear separation between Infrastructure (LogFile), Presentation (Dispatcher), and Application (Cases) layers.
- **Reliability**: Asynchronous task management prevents system bottlenecks.


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