# Gpgram Examples

This directory contains examples demonstrating various features of the Gpgram library.

## Examples

### Basic Examples

- [`echo_bot.py`](echo_bot.py) - Simple echo bot that repeats messages
- [`command_bot.py`](command_bot.py) - Bot with command handling
- [`markdown_bot.py`](markdown_bot.py) - Bot demonstrating Markdown formatting

### Advanced Examples

- [`media_bot.py`](media_bot.py) - Bot handling photos, documents, and media
- [`keyboard_bot.py`](keyboard_bot.py) - Bot with reply keyboards
- [`inline_keyboard_bot.py`](inline_keyboard_bot.py) - Bot with inline keyboards and callbacks
- [`webhook_bot.py`](webhook_bot.py) - Bot using webhooks instead of polling

## Running Examples

1. Install Gpgram:
```bash
pip install gpgram
```

2. Set your bot token as an environment variable:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

3. Run any example:
```bash
python examples/echo_bot.py
```

## Bot Token

All examples require a Telegram bot token. You can get one by:
1. Messaging [@BotFather](https://t.me/botfather) on Telegram
2. Using the `/newbot` command
3. Following the instructions to create your bot

## Example Structure

Each example follows this pattern:

```python
from gpgram import Bot

bot = Bot("YOUR_BOT_TOKEN")

# Define handlers using decorators
@bot.command(r"start")
async def start(event):
    await event.send_message("Hello! I'm a Gpgram bot.")

# Run the bot
bot.run()
```

## Features Demonstrated

- **Commands**: `/start`, `/help`, custom commands
- **Messages**: Text, photos, documents, media
- **Keyboards**: Reply keyboards, inline keyboards
- **Callbacks**: Inline button callbacks
- **Formatting**: Markdown, HTML text formatting
- **Webhooks**: HTTP webhook integration
- **Error Handling**: Proper error handling patterns