# Gpgram Examples

This directory contains example bots created with Gpgram.

## Prerequisites

Before running the examples, make sure you have:

1. Created a Telegram bot using [BotFather](https://t.me/botfather)
2. Obtained your bot token
3. Installed the Gpgram package (`pip install -e ..` from this directory)

## Running the Examples

### Setting the Bot Token

You need to set your Telegram bot token as an environment variable:

```bash
# Linux/macOS
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Windows (Command Prompt)
set TELEGRAM_BOT_TOKEN=your_bot_token_here

# Windows (PowerShell)
$env:TELEGRAM_BOT_TOKEN = "your_bot_token_here"
```

### Running a Bot

```bash
# Run the simple bot
python simple_bot.py

# Run the echo bot
python echo_bot.py

# Run the inline keyboard bot
python inline_keyboard_bot.py

# Run the advanced bot
python advanced_bot.py

# Run the test bot
python test.py
```

## Example Bots

### Simple Bot

A simple bot with basic commands.

### Echo Bot

A bot that echoes back messages.

### Inline Keyboard Bot

A bot demonstrating the use of inline keyboards.

### Advanced Bot

An advanced bot with inline keyboards, middleware, and error handling.

### Test Bot

A simple test bot that combines features from the other examples.
