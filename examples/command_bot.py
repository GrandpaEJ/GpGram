#!/usr/bin/env python3
"""
Command Bot Example

A bot that demonstrates various command handling patterns.
Shows how to handle commands with and without parameters.
"""

import os

from gpgram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Please set TELEGRAM_BOT_TOKEN environment variable")
    exit(1)

bot = Bot(TOKEN)

@bot.command(r"start")
async def start(event):
    """Welcome message with available commands."""
    welcome_text = """
🎉 *Welcome to Command Bot!*

I'm here to demonstrate various command patterns:

*Basic Commands:*
/start - Show this welcome message
/help - Show detailed help
/info - Get bot information

*Commands with Parameters:*
/greet John - Greet someone by name
/calc 5 + 3 - Simple calculator
/reverse hello - Reverse text

*Regex Commands:*
/sayhi or /hi or /hello - Multiple greetings
/time - Show current time

Try them out! 🚀
"""
    await event.send_message(welcome_text, parse_mode="Markdown")

@bot.command(r"help")
async def help_command(event):
    """Detailed help information."""
    help_text = """
📚 *Command Bot - Help Guide*

*Command Patterns:*
• Exact match: `/start`
• With parameters: `/greet John`
• Regex patterns: `/sayhi|/hi|/hello`

*Examples:*
/greet Alice → "Hello, Alice!"
/calc 10 * 5 → "Result: 50"
/reverse world → "dlrow"
/time → Current timestamp

*Tips:*
• Commands are case-sensitive
• Parameters are separated by spaces
• Use quotes for multi-word parameters

Have fun exploring! 🎈
"""
    await event.send_message(help_text, parse_mode="Markdown")

@bot.command(r"info")
async def info(event):
    """Show bot information."""
    info_text = f"""
🤖 *Bot Information*

• **Name:** Command Bot
• **Framework:** Gpgram v1.0.0
• **Language:** Python 3.12+
• **User ID:** {event.user_id}
• **Chat ID:** {event.chat_id}

This bot demonstrates advanced command handling with regex patterns and parameter parsing.
"""
    await event.send_message(info_text, parse_mode="Markdown")

@bot.command(r"greet (\w+)")
async def greet(event):
    """Greet someone by name - captures one word parameter."""
    name = event.text  # The regex capture group
    await event.reply(f"Hello, {name}! 👋")

@bot.command(r"calc (\d+) ([\+\-\*\/]) (\d+)")
async def calculator(event):
    """Simple calculator with regex pattern matching."""
    # Extract numbers and operator from regex groups
    parts = event.text.split()
    if len(parts) >= 4:
        try:
            num1 = int(parts[1])
            operator = parts[2]
            num2 = int(parts[3])

            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 == 0:
                    await event.reply("❌ Cannot divide by zero!")
                    return
                result = num1 / num2
            else:
                await event.reply("❌ Invalid operator!")
                return

            await event.reply(f"📊 Result: {num1} {operator} {num2} = {result}")

        except ValueError:
            await event.reply("❌ Invalid numbers!")
    else:
        await event.reply("Usage: /calc <number> <operator> <number>")

@bot.command(r"reverse (.+)")
async def reverse_text(event):
    """Reverse any text."""
    text_to_reverse = event.text  # Captured group
    reversed_text = text_to_reverse[::-1]
    await event.reply(f"🔄 Reversed: {reversed_text}")

@bot.command(r"sayhi|hi|hello")
async def multiple_greetings(event):
    """Handle multiple similar commands with regex OR."""
    command = event.text.split()[0][1:]  # Extract command without /
    responses = {
        "sayhi": "Hi there! 😊",
        "hi": "Hey! 👋",
        "hello": "Hello! 🤗"
    }
    await event.reply(responses.get(command, "Greetings! 🎉"))

@bot.command(r"time")
async def current_time(event):
    """Show current timestamp."""
    import time
    current_time = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    await event.reply(f"🕐 Current time: {current_time}")

@bot.on_message(r"^(?!/).+")  # Match any message that doesn't start with /
async def unknown_command(event):
    """Handle non-command messages."""
    await event.reply(
        "🤔 I didn't understand that command.\n\n"
        "Try /help to see available commands!"
    )

if __name__ == "__main__":
    print("🚀 Starting Command Bot...")
    print("Try commands like: /start, /greet John, /calc 5 + 3, /reverse hello")
    bot.run()
