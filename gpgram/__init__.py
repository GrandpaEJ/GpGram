"""
Gpgram - A clean and simple Telegram Bot API library.

This library provides a straightforward, event-driven interface for building
Telegram bots with minimal complexity and maximum ease of use.

Example:
    from gpgram import Bot

    bot = Bot("YOUR_BOT_TOKEN")

    @bot.command(r"hello|hi")
    async def greet(event):
        await event.send_message("Hello there!")

    @bot.on_message(r"ping")
    async def ping(event):
        await event.reply("Pong!")

    bot.run()
"""

__version__ = "1.0.0"

from .bot import Bot, Event

__all__ = ["Bot", "Event"]
