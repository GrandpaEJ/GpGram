#!/usr/bin/env python3
"""
Markdown Bot Example

Demonstrates various Markdown formatting options available in Telegram.
Shows how to use bold, italic, code blocks, links, and more.
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
    """Show welcome message with formatting examples."""
    welcome_text = """
🎨 *Markdown Formatting Bot*

I can show you all the *fancy* formatting options available in Telegram!

Try these commands:
/bold - Bold text examples
/italic - Italic text examples
/code - Code and code blocks
/links - Links and mentions
/lists - Lists and quotes
/all - See everything at once

Send /help for more info!
"""
    await event.send_message(welcome_text, parse_mode="Markdown")

@bot.command(r"bold")
async def bold_examples(event):
    """Demonstrate bold text formatting."""
    bold_text = """
**Bold Text Examples:**

• **This is bold text**
• Normal text with **bold words** in between
• ***Bold and italic*** combined
• __This is also bold__ (alternative syntax)

*Note:* Telegram supports both **double asterisks** and __double underscores__ for bold.
"""
    await event.send_message(bold_text, parse_mode="Markdown")

@bot.command(r"italic")
async def italic_examples(event):
    """Demonstrate italic text formatting."""
    italic_text = """
*Italic Text Examples:*

• *This is italic text*
• Normal text with *italic words* mixed in
• **Bold and *italic* combined**
• _This is also italic_ (alternative syntax)

*Note:* Telegram supports both *single asterisks* and _single underscores_ for italic.
"""
    await event.send_message(italic_text, parse_mode="Markdown")

@bot.command(r"code")
async def code_examples(event):
    """Demonstrate code formatting."""
    code_text = """
`Inline Code` and Code Blocks:

`This is inline code`

```python
# This is a code block
def hello_world():
    print("Hello, World!")
    return "success"
```

```javascript
// JavaScript code block
const greet = (name) => {
    return `Hello, ${name}!`;
};
```

```bash
# Bash commands
echo "Hello from terminal"
pip install gpgram
```

*Tip:* Use `backticks` for inline code and ```triple backticks``` for code blocks.
"""
    await event.send_message(code_text, parse_mode="Markdown")

@bot.command(r"links")
async def links_examples(event):
    """Demonstrate links and mentions."""
    links_text = """
🔗 Links and Mentions:

• [Click here for Gpgram docs](https://gpgram.readthedocs.io/)
• [GitHub Repository](https://github.com/yourusername/gpgram)
• Visit gpgram.com for more info

*User Mentions:*
• Regular mention: @username
• Hidden mention: [John Doe](tg://user?id=123456789)

*Note:* User mentions only work in supergroups and channels.
"""
    await event.send_message(links_text, parse_mode="Markdown")

@bot.command(r"lists")
async def lists_examples(event):
    """Demonstrate lists and quotes."""
    lists_text = """
📝 Lists and Quotes:

*Unordered Lists:*
• Item 1
• Item 2
  • Nested item 2.1
  • Nested item 2.2
• Item 3

*Ordered Lists:*
1. First item
2. Second item
   1. Nested numbered item
   2. Another nested item
3. Third item

> This is a blockquote
> It can span multiple lines
> And contain *formatting*

*Note:* Use • or - or * for unordered lists, numbers for ordered lists.
"""
    await event.send_message(lists_text, parse_mode="Markdown")

@bot.command(r"all")
async def all_formatting(event):
    """Show all formatting options at once."""
    all_text = """
🎨 **Complete Markdown Guide**

*Text Formatting:*
• **Bold text** and *italic text*
• ***Bold italic*** and `inline code`
• ~~Strikethrough~~ (if supported)

*Code Blocks:*
```python
def example():
    return "Hello, Markdown!"
```

*Links & Mentions:*
• [Gpgram Docs](https://gpgram.readthedocs.io/)
• @username mentions

*Lists:*
1. Ordered list item
2. Another item
• Unordered item
• Another bullet

> Blockquote with *formatting*

*Headers:*
# H1 Header
## H2 Header
### H3 Header

*Note:* Not all formatting works in all contexts. Test in your bot!
"""
    await event.send_message(all_text, parse_mode="Markdown")

@bot.command(r"help")
async def help_command(event):
    """Show help information."""
    help_text = """
📚 *Markdown Bot Help*

This bot demonstrates Telegram's Markdown formatting capabilities.

*Available Commands:*
/start - Welcome message
/bold - Bold text examples
/italic - Italic text examples
/code - Code formatting examples
/links - Links and mentions
/lists - Lists and blockquotes
/all - Complete formatting guide
/help - This help message

*Tips:*
• Use `parse_mode="Markdown"` when sending messages
• Not all formatting works everywhere
• Test formatting in different chat types
• Some features require Telegram Premium

Try the commands above to see formatting in action! 🎨
"""
    await event.send_message(help_text, parse_mode="Markdown")

@bot.on_message(r"^(?!/).+")  # Match any non-command message
async def unknown_message(event):
    """Handle non-command messages by showing formatting help."""
    await event.reply(
        "🤔 I only respond to commands!\n\n"
        "Try /start to see available formatting examples.",
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print("🚀 Starting Markdown Bot...")
    print("Try commands like: /bold, /code, /links, /all")
    bot.run()
