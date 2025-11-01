#!/usr/bin/env python3
"""
Media Bot Example

Demonstrates how to handle various media types in Gpgram:
- Photos and images
- Documents and files
- Audio and voice messages
- Videos and animations
- Stickers
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
    """Show welcome message with media examples."""
    welcome_text = """
🎬 *Media Bot*

I can handle all types of media! Try these commands:

*Photo Commands:*
/photo - Send a sample photo
/photo_url - Send photo from URL
/photo_file - Send local photo file

*Document Commands:*
/document - Send a document
/document_url - Send document from URL

*Other Media:*
/animation - Send GIF animation
/audio - Send audio file
/voice - Send voice message
/video - Send video
/sticker - Send sticker

*Interactive:*
/media_keyboard - Show media options keyboard

Send me photos, documents, or other media to see info about them!
"""
    await event.send_message(welcome_text, parse_mode="Markdown")

@bot.command(r"photo")
async def send_photo(event):
    """Send a sample photo with caption."""
    # Using a sample image URL (this is a placeholder - replace with real URL)
    photo_url = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=Gpgram+Bot"

    await event.send_message(
        "📸 Here's a sample photo:",
        photo=photo_url,
        caption="This is a sample photo sent by Gpgram bot! 🖼️"
    )

@bot.command(r"photo_url")
async def send_photo_from_url(event):
    """Send photo from a URL."""
    # Using a different sample image
    photo_url = "https://via.placeholder.com/500x400/2196F3/FFFFFF?text=URL+Photo"

    await event.send_message(
        "🌐 Photo loaded from URL:",
        photo=photo_url,
        caption="This photo was loaded from a URL! 🔗"
    )

@bot.command(r"document")
async def send_document(event):
    """Send a sample document."""
    # Create a simple text file to send as document
    import tempfile
    import io

    # Create sample content
    content = """Hello from Gpgram Media Bot! 📄

This is a sample document demonstrating document sending capabilities.

Features demonstrated:
• Document upload
• File handling
• Caption support
• MIME type detection

Gpgram makes media handling simple! 🚀
"""

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        temp_file_path = f.name

    try:
        # Send the file as a document
        await event.send_message(
            document=temp_file_path,
            caption="📄 Sample document created and sent by the bot!"
        )
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

@bot.command(r"animation")
async def send_animation(event):
    """Send an animated GIF."""
    # Using a sample GIF URL (placeholder)
    gif_url = "https://media.giphy.com/media/3o7TKz9bX9Z9Z9Z9Z9/giphy.gif"

    await event.send_message(
        "🎞️ Here's an animation:",
        animation=gif_url,
        caption="Animated GIF sent via Gpgram! 🎉"
    )

@bot.command(r"audio")
async def send_audio(event):
    """Send an audio file."""
    # Note: In a real bot, you'd have actual audio files
    # This is just a demonstration of the API
    await event.send_message(
        "🎵 *Audio Support*\n\n"
        "Audio file sending would work like this:\n"
        "```python\n"
        "await event.send_message(\n"
        "    audio='path/to/audio.mp3',\n"
        "    caption='Great song!',\n"
        "    title='Song Title',\n"
        "    performer='Artist Name'\n"
        ")\n"
        "```",
        parse_mode="Markdown"
    )

@bot.command(r"video")
async def send_video(event):
    """Send a video file."""
    # Using a sample video URL (placeholder)
    video_url = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"

    await event.send_message(
        "🎥 *Video Support*\n\n"
        "Video sending would work like this:\n"
        "```python\n"
        "await event.send_message(\n"
        "    video='path/to/video.mp4',\n"
        "    caption='Check out this video!',\n"
        "    width=640,\n"
        "    height=480\n"
        ")\n"
        "```",
        parse_mode="Markdown"
    )

@bot.command(r"sticker")
async def send_sticker(event):
    """Send a sticker."""
    await event.send_message(
        "🏷️ *Sticker Support*\n\n"
        "Stickers can be sent using file IDs or URLs:\n"
        "```python\n"
        "await event.send_message(\n"
        "    sticker='sticker_file_id'\n"
        ")\n"
        "```\n\n"
        "*Note:* Sticker file IDs are obtained when users send stickers to your bot.",
        parse_mode="Markdown"
    )

@bot.command(r"media_keyboard")
async def media_keyboard(event):
    """Show an inline keyboard with media options."""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📸 Photo", "callback_data": "media_photo"},
                {"text": "📄 Document", "callback_data": "media_document"}
            ],
            [
                {"text": "🎞️ Animation", "callback_data": "media_animation"},
                {"text": "🎵 Audio", "callback_data": "media_audio"}
            ],
            [
                {"text": "🎥 Video", "callback_data": "media_video"},
                {"text": "🏷️ Sticker", "callback_data": "media_sticker"}
            ]
        ]
    }

    await event.send_message(
        "🎬 Choose a media type to learn more:",
        reply_markup=keyboard
    )

@bot.on_callback(r"media_(\w+)")
async def handle_media_callbacks(event):
    """Handle media keyboard callbacks."""
    media_type = event.callback_data.split("_")[1]

    responses = {
        "photo": "📸 *Photos*\n\nSend photos using:\n```python\nawait event.send_message(photo='image.jpg', caption='Caption')\n```",
        "document": "📄 *Documents*\n\nSend files using:\n```python\nawait event.send_message(document='file.pdf', caption='Document')\n```",
        "animation": "🎞️ *Animations*\n\nSend GIFs using:\n```python\nawait event.send_message(animation='anim.gif')\n```",
        "audio": "🎵 *Audio*\n\nSend music using:\n```python\nawait event.send_message(audio='song.mp3', title='Title', performer='Artist')\n```",
        "video": "🎥 *Videos*\n\nSend videos using:\n```python\nawait event.send_message(video='movie.mp4', caption='Video')\n```",
        "sticker": "🏷️ *Stickers*\n\nSend stickers using:\n```python\nawait event.send_message(sticker='sticker_id')\n```"
    }

    response = responses.get(media_type, "Unknown media type")
    await event.edit_message(response, parse_mode="Markdown")
    await event.answer_callback(f"Showing {media_type} info!")

# Media event handlers - respond when users send media
@bot.on_message()  # This will catch all messages including media
async def handle_incoming_media(event):
    """Handle incoming media messages."""
    # Check what type of media was sent
    if hasattr(event, 'photo') and event.photo:
        await event.reply("📸 I received a photo! Nice picture! 🖼️")

    elif hasattr(event, 'document') and event.document:
        doc = event.document
        file_name = doc.get('file_name', 'Unknown')
        file_size = doc.get('file_size', 0)
        await event.reply(f"📄 Document received: {file_name} ({file_size} bytes)")

    elif hasattr(event, 'audio') and event.audio:
        audio = event.audio
        title = audio.get('title', 'Unknown')
        duration = audio.get('duration', 0)
        await event.reply(f"🎵 Audio received: {title} ({duration}s)")

    elif hasattr(event, 'video') and event.video:
        video = event.video
        duration = video.get('duration', 0)
        width = video.get('width', 0)
        height = video.get('height', 0)
        await event.reply(f"🎥 Video received: {width}x{height}, {duration}s")

    elif hasattr(event, 'animation') and event.animation:
        await event.reply("🎞️ Nice animation! GIFs are cool! 🎉")

    elif hasattr(event, 'sticker') and event.sticker:
        await event.reply("🏷️ Cute sticker! 😊")

    elif hasattr(event, 'voice') and event.voice:
        duration = event.voice.get('duration', 0)
        await event.reply(f"🎤 Voice message received ({duration}s)")

    # Only respond to media messages, ignore text
    elif event.text and not event.text.startswith('/'):
        return  # Don't respond to regular text messages

if __name__ == "__main__":
    print("🚀 Starting Media Bot...")
    print("Try commands like: /photo, /document, /media_keyboard")
    print("Or send me photos, documents, or other media!")
    bot.run()