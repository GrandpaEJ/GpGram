# Examples

Here are some examples of how to use Gpgram.

## Simple Bot

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

## Echo Bot

```python
import asyncio
import os
from gpgram import Bot, Dispatcher, Router

# Create a router
router = Router()

# Echo all messages
@router.message()
async def echo_message(message, bot):
    if message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You said: {message.text}"
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="I can only echo text messages!"
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

## Inline Keyboard Bot

```python
import asyncio
import os
from gpgram import Bot, Dispatcher, Router, CommandFilter
from gpgram.utils import InlineKeyboardBuilder

# Create a router
router = Router()

# Register a command handler
@router.message(CommandFilter('start'))
async def start_command(message, bot):
    # Create an inline keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.add_button(text="Option 1", callback_data="option1")
    keyboard.add_button(text="Option 2", callback_data="option2")
    keyboard.row()
    keyboard.add_button(text="Help", callback_data="help")
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Please select an option:",
        reply_markup=keyboard.as_markup()
    )

# Handle callback queries
@router.callback_query()
async def callback_handler(callback_query, bot):
    data = callback_query.data
    
    if data == "option1":
        text = "You selected Option 1"
    elif data == "option2":
        text = "You selected Option 2"
    elif data == "help":
        text = "This is a help message"
    else:
        text = "Unknown option"
    
    await bot.answer_callback_query(
        callback_query_id=callback_query.id,
        text=text
    )
    
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=text
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
