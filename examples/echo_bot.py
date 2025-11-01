#!/usr/bin/env python3
"""
Echo Bot Example

A simple bot that echoes back any message it receives.
This demonstrates basic message handling in Gpgram.
"""

import os

from gpgram import Bot

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Please set TELEGRAM_BOT_TOKEN environment variable")
    exit(1)

bot = Bot(TOKEN)

@bot.on_message()
async def echo(event):
    """
    Echo back any message received.

    This handler catches all messages and replies with the same text.
    """
    await event.reply(f"You said: {event.text}")

@bot.command(r"start")
async def start(event):
    """Handle the /start command."""
    await event.send_message(
        "👋 Hello! I'm an echo bot.\n\n"
        "Send me any message and I'll echo it back!\n"
        "Try: /help"
    )

@bot.command(r"help")
async def help_command(event):
    """Handle the /help command."""
    help_text = """
🤖 *Echo Bot Help*

I repeat everything you say! Try sending me:
• Text messages
• Commands
• Any other content

*Commands:*
/start - Show welcome message
/help - Show this help

Just send me a message and see what happens! 🎉
"""
    await event.send_message(help_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("🚀 Starting Echo Bot...")
    print("Send me a message and I'll echo it back!")
    bot.run()
