#!/usr/bin/env python3
"""
Keyboard Bot Example

Demonstrates reply keyboards and inline keyboards in Gpgram.
Shows how to create interactive button interfaces for users.
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
    """Show welcome message with keyboard options."""
    welcome_text = """
⌨️ *Keyboard Bot*

I demonstrate different types of keyboards in Telegram!

*Commands:*
/reply_keyboard - Show reply keyboard
/inline_keyboard - Show inline keyboard
/remove_keyboard - Remove current keyboard
/keyboard_help - More info about keyboards

*Reply Keyboards:*
• Appear above the message input field
• Always visible until removed
• Good for frequently used options

*Inline Keyboards:*
• Appear below messages
• Can be edited or removed
• Support callbacks for interaction

Try the commands above! 🎹
"""
    await event.send_message(welcome_text, parse_mode="Markdown")

@bot.command(r"reply_keyboard")
async def show_reply_keyboard(event):
    """Show a reply keyboard with various options."""
    keyboard = {
        "keyboard": [
            ["📅 Today", "📅 Tomorrow", "📅 This Week"],
            ["🎯 High Priority", "⚡ Normal", "🐌 Low"],
            ["✅ Done", "❌ Cancel"],
            ["🔙 Back to Main"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "input_field_placeholder": "Choose an option..."
    }

    await event.send_message(
        "⌨️ *Reply Keyboard Demo*\n\n"
        "This keyboard stays visible until you remove it.\n"
        "Try pressing different buttons!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.command(r"inline_keyboard")
async def show_inline_keyboard(event):
    """Show an inline keyboard with callback buttons."""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "👍 Like", "callback_data": "action_like"},
                {"text": "👎 Dislike", "callback_data": "action_dislike"}
            ],
            [
                {"text": "⭐ Favorite", "callback_data": "action_favorite"},
                {"text": "🔗 Share", "callback_data": "action_share"}
            ],
            [
                {"text": "📊 Stats", "callback_data": "action_stats"},
                {"text": "⚙️ Settings", "callback_data": "action_settings"}
            ]
        ]
    }

    await event.send_message(
        "🎮 *Inline Keyboard Demo*\n\n"
        "These buttons appear below the message.\n"
        "Click them to see callback responses!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.command(r"remove_keyboard")
async def remove_keyboard(event):
    """Remove the current reply keyboard."""
    # Send a message with an empty keyboard to remove it
    keyboard = {"remove_keyboard": True}

    await event.send_message(
        "⌨️ Keyboard removed!\n\n"
        "The reply keyboard has been removed.\n"
        "Use /reply_keyboard to show it again.",
        reply_markup=keyboard
    )

@bot.command(r"keyboard_help")
async def keyboard_help(event):
    """Show detailed information about keyboards."""
    help_text = """
📚 *Keyboard Guide*

*Reply Keyboards:*
• Always visible above input field
• Can be resized and customized
• Stay until explicitly removed
• Good for: Menus, forms, persistent options

*Inline Keyboards:*
• Appear below specific messages
• Support rich interactions via callbacks
• Can be edited or removed independently
• Good for: Polls, actions, dynamic content

*Creating Keyboards:*

*Reply Keyboard:*
```python
keyboard = {
    "keyboard": [
        ["Button 1", "Button 2"],
        ["Button 3"]
    ],
    "resize_keyboard": True
}
```

*Inline Keyboard:*
```python
keyboard = {
    "inline_keyboard": [
        [
            {"text": "👍", "callback_data": "like"},
            {"text": "👎", "callback_data": "dislike"}
        ]
    ]
}
```

*Commands:*
/reply_keyboard - Show reply keyboard
/inline_keyboard - Show inline keyboard
/remove_keyboard - Remove reply keyboard
"""
    await event.send_message(help_text, parse_mode="Markdown")

# Handle reply keyboard button presses
@bot.on_message(r"📅 (.+)")
async def handle_date_buttons(event):
    """Handle date selection from reply keyboard."""
    date_option = event.text.replace("📅 ", "")
    await event.reply(f"📅 You selected: {date_option}")

@bot.on_message(r"🎯 (.+)")
async def handle_priority_buttons(event):
    """Handle priority selection."""
    priority = event.text.replace("🎯 ", "")
    await event.reply(f"🎯 Priority set to: {priority}")

@bot.on_message(r"⚡ (.+)")
async def handle_normal_priority(event):
    """Handle normal priority."""
    await event.reply("⚡ Normal priority selected!")

@bot.on_message(r"🐌 (.+)")
async def handle_low_priority(event):
    """Handle low priority."""
    await event.reply("🐌 Low priority selected!")

@bot.on_message(r"✅ (.+)")
async def handle_done(event):
    """Handle done action."""
    await event.reply("✅ Task marked as done!")

@bot.on_message(r"❌ (.+)")
async def handle_cancel(event):
    """Handle cancel action."""
    await event.reply("❌ Action cancelled.")

@bot.on_message(r"🔙 (.+)")
async def handle_back(event):
    """Handle back to main menu."""
    await event.reply("🔙 Back to main menu!")

# Handle inline keyboard callbacks
@bot.on_callback(r"action_like")
async def handle_like(event):
    """Handle like button callback."""
    await event.answer_callback("👍 You liked this!")
    await event.edit_message(
        "👍 *Liked!*\n\nThank you for the positive feedback!",
        parse_mode="Markdown"
    )

@bot.on_callback(r"action_dislike")
async def handle_dislike(event):
    """Handle dislike button callback."""
    await event.answer_callback("👎 Feedback noted")
    await event.edit_message(
        "👎 *Disliked*\n\nWe'll work on improving!",
        parse_mode="Markdown"
    )

@bot.on_callback(r"action_favorite")
async def handle_favorite(event):
    """Handle favorite button callback."""
    await event.answer_callback("⭐ Added to favorites!")
    await event.edit_message(
        "⭐ *Favorited!*\n\nSaved to your favorites list.",
        parse_mode="Markdown"
    )

@bot.on_callback(r"action_share")
async def handle_share(event):
    """Handle share button callback."""
    await event.answer_callback("🔗 Share link copied!")
    await event.edit_message(
        "🔗 *Share*\n\nShare link: `https://t.me/share/url?url=...`",
        parse_mode="Markdown"
    )

@bot.on_callback(r"action_stats")
async def handle_stats(event):
    """Handle stats button callback."""
    await event.answer_callback("📊 Loading stats...")
    await event.edit_message(
        "📊 *Statistics*\n\n"
        "• 👍 Likes: 42\n"
        "• 👎 Dislikes: 3\n"
        "• ⭐ Favorites: 15\n"
        "• 🔗 Shares: 8",
        parse_mode="Markdown"
    )

@bot.on_callback(r"action_settings")
async def handle_settings(event):
    """Handle settings button callback."""
    # Create a new inline keyboard for settings
    settings_keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔔 Notifications", "callback_data": "setting_notifications"},
                {"text": "🌙 Theme", "callback_data": "setting_theme"}
            ],
            [
                {"text": "🔒 Privacy", "callback_data": "setting_privacy"},
                {"text": "❓ Help", "callback_data": "setting_help"}
            ],
            [
                {"text": "⬅️ Back", "callback_data": "back_to_main"}
            ]
        ]
    }

    await event.edit_message(
        "⚙️ *Settings*\n\nChoose a setting to configure:",
        reply_markup=settings_keyboard,
        parse_mode="Markdown"
    )
    await event.answer_callback("⚙️ Opening settings...")

@bot.on_callback(r"setting_(\w+)")
async def handle_settings_options(event):
    """Handle settings submenu callbacks."""
    setting = event.callback_data.split("_")[1]

    responses = {
        "notifications": "🔔 *Notifications*\n\nConfigure your notification preferences.",
        "theme": "🌙 *Theme*\n\nChoose light or dark theme.",
        "privacy": "🔒 *Privacy*\n\nManage your privacy settings.",
        "help": "❓ *Help*\n\nGet help with bot settings."
    }

    response = responses.get(setting, "Unknown setting")
    await event.edit_message(response, parse_mode="Markdown")
    await event.answer_callback(f"Opening {setting} settings...")

@bot.on_callback(r"back_to_main")
async def back_to_main(event):
    """Go back to main inline keyboard."""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "👍 Like", "callback_data": "action_like"},
                {"text": "👎 Dislike", "callback_data": "action_dislike"}
            ],
            [
                {"text": "⭐ Favorite", "callback_data": "action_favorite"},
                {"text": "🔗 Share", "callback_data": "action_share"}
            ],
            [
                {"text": "📊 Stats", "callback_data": "action_stats"},
                {"text": "⚙️ Settings", "callback_data": "action_settings"}
            ]
        ]
    }

    await event.edit_message(
        "🎮 *Back to Main Menu*\n\nChoose an action:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await event.answer_callback("⬅️ Back to main menu")

if __name__ == "__main__":
    print("🚀 Starting Keyboard Bot...")
    print("Try: /reply_keyboard, /inline_keyboard, /keyboard_help")
    bot.run()