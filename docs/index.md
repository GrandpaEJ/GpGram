# Gpgram Documentation

Welcome to the Gpgram documentation! Gpgram is a modern, asynchronous Telegram Bot API library with advanced handler capabilities.

## Installation

```bash
pip install gpgram
```

## Quick Start

```python
import asyncio
import os
from gpgram import Bot, Dispatcher, Router, CommandFilter

# Create a router
router = Router()

# Register a command handler
@router.message(CommandFilter('start'))
async def start_command(message, bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm a bot created with Gpgram."
    )

async def main():
    # Get the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    # Create a bot instance
    bot = Bot(token=token)
    
    # Create a dispatcher
    dp = Dispatcher(bot=bot)
    
    # Register the router with the dispatcher
    dp.register_router(router)
    
    # Start polling
    await dp.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Asynchronous API
- Type hints and validation with Pydantic
- Advanced routing system
- Middleware support
- Comprehensive error handling
- Loguru integration for advanced logging

## API Reference

For detailed API documentation, see the [API Reference](api_reference.md).

## Examples

For more examples, see the [Examples](examples.md) section.
