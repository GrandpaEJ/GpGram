# Gpgram

A clean and simple Telegram Bot API library for Python.

## Features

- 🚀 **Simple API** - Clean, event-driven design with decorator-based handlers
- ⚡ **Fast** - Built with async/await and httpx for high performance
- 🛡️ **Type Safe** - Full type hints with Pydantic models
- 🧪 **Well Tested** - Comprehensive test suite with pytest
- 📦 **Modern** - Uses modern Python practices and tools

## Installation

```bash
pip install gpgram
```

## Quick Start

```python
from gpgram import Bot

bot = Bot("YOUR_BOT_TOKEN")

@bot.command(r"hello|hi")
async def greet(event):
    await event.send_message("Hello there!")

@bot.on_message(r"ping")
async def ping(event):
    await event.reply("Pong!")

@bot.on_callback(r"data")
async def handle_callback(event):
    await event.answer_callback("Callback received!")

bot.run()
```

## API Reference

### Bot Class

#### Constructor
```python
Bot(token: str, timeout: float = 30.0, api_url: Optional[str] = None)
```

#### Decorators

- `@bot.command(pattern)` - Handle commands with regex pattern matching
- `@bot.on_message(pattern)` - Handle messages with regex pattern matching
- `@bot.on_callback(pattern)` - Handle callback queries with regex pattern matching

#### Methods

- `bot.send_message(chat_id, text, **kwargs)` - Send a text message
- `bot.edit_message_text(text, chat_id, message_id, **kwargs)` - Edit a message
- `bot.delete_message(chat_id, message_id)` - Delete a message
- `bot.answer_callback_query(callback_query_id, text, **kwargs)` - Answer callback query
- `bot.polling(**kwargs)` - Start polling for updates
- `bot.run()` - Run the bot (blocking)

### Event Class

#### Properties

- `event.message` - Message object (if available)
- `event.callback_query` - Callback query object (if available)
- `event.text` - Message text
- `event.callback_data` - Callback data
- `event.chat_id` - Chat ID
- `event.user_id` - User ID

#### Methods

- `event.send_message(text, **kwargs)` - Send message to event chat
- `event.reply(text, **kwargs)` - Reply to the event
- `event.edit_message(text, **kwargs)` - Edit the message
- `event.delete_message()` - Delete the message
- `event.answer_callback(text, **kwargs)` - Answer callback query

## Examples

### Command Handling

```python
@bot.command(r"start")
async def start(event):
    await event.send_message("Welcome! Use /help for commands.")

@bot.command(r"echo (.+)")
async def echo(event):
    # Extract captured group from regex
    message = event.text  # This would be "echo hello world"
    await event.reply(f"You said: {message}")
```

### Message Handling

```python
@bot.on_message(r"hello")
async def hello(event):
    await event.reply("Hi there!")

@bot.on_message(r"buy (.+)")
async def buy(event):
    item = event.text.split(" ", 1)[1]
    await event.send_message(f"You want to buy: {item}")
```

### Callback Queries

```python
@bot.on_callback(r"page_(\d+)")
async def pagination(event):
    page = int(event.callback_data.split("_")[1])
    await event.edit_message(f"Page {page}")
    await event.answer_callback()
```

### Inline Keyboards

```python
from gpgram import Bot

bot = Bot("token")

@bot.command(r"menu")
async def show_menu(event):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Button 1", "callback_data": "btn1"},
                {"text": "Button 2", "callback_data": "btn2"}
            ]
        ]
    }

    await event.send_message("Choose an option:", reply_markup=keyboard)

@bot.on_callback(r"btn1|btn2")
async def handle_buttons(event):
    await event.edit_message(f"You clicked: {event.callback_data}")
    await event.answer_callback("Button clicked!")

bot.run()
```

## Development

### Setup

```bash
git clone https://github.com/GrandpaEJ/gpgram.git
cd gpgram
uv sync --dev
```

### Testing

```bash
uv run pytest
```

### Code Quality

```bash
uv run black gpgram/ tests/
uv run ruff check gpgram/ tests/
uv run flake8 gpgram/ tests/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
