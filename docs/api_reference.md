# API Reference

## Bot

The `Bot` class is the main interface to the Telegram Bot API.

```python
from gpgram import Bot

bot = Bot(token="YOUR_BOT_TOKEN")
```

### Methods

- `get_me()` - Get information about the bot
- `get_updates()` - Get updates from Telegram
- `send_message()` - Send a message
- `send_photo()` - Send a photo
- `send_document()` - Send a document
- `answer_callback_query()` - Answer a callback query
- `edit_message_text()` - Edit a message's text

## Dispatcher

The `Dispatcher` class handles the routing of updates to the appropriate handlers.

```python
from gpgram import Bot, Dispatcher

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot=bot)
```

### Methods

- `register_router()` - Register a router
- `register_middleware()` - Register middleware
- `register_error_handler()` - Register an error handler
- `run_polling()` - Start polling for updates

## Router

The `Router` class provides a way to organize handlers.

```python
from gpgram import Router

router = Router()
```

### Methods

- `message()` - Register a message handler
- `callback_query()` - Register a callback query handler
- `inline_query()` - Register an inline query handler

## Filters

Filters are used to determine whether a handler should process an update.

```python
from gpgram.filters import CommandFilter, TextFilter, RegexFilter

# Command filter
@router.message(CommandFilter('start'))
async def start_command(message, bot):
    # ...

# Text filter
@router.message(TextFilter('hello'))
async def hello_handler(message, bot):
    # ...

# Regex filter
@router.message(RegexFilter(r'\d+'))
async def number_handler(message, bot):
    # ...
```

## Types

Gpgram provides Pydantic models for Telegram API types.

```python
from gpgram.types import Message, User, Chat, Update

# Access message properties
@router.message()
async def message_handler(message: Message, bot):
    user = message.from_user
    chat = message.chat
    text = message.text
    # ...
```

## Middleware

Middleware allows you to process updates before and after they are handled.

```python
from gpgram.middleware import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update, data):
        # Log incoming update
        self.logger.info(f"Received update: {update.update_id}")
    
    async def on_post_process_update(self, update, data, handler_result):
        # Log after handling
        self.logger.info(f"Handled update: {update.update_id}")

# Register middleware
dp.register_middleware(LoggingMiddleware())
```

## Logging

Gpgram uses Loguru for advanced logging.

```python
from gpgram.logging import setup_logging

# Configure logging
setup_logging(
    level="INFO",
    file="bot.log",
    json=True
)
```
