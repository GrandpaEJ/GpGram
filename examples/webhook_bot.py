#!/usr/bin/env python3
"""
Webhook Bot Example

Demonstrates how to use webhooks instead of polling for updates.
Webhooks are more efficient for production bots as they don't require constant polling.
"""

import os
import asyncio
from gpgram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Please set TELEGRAM_BOT_TOKEN environment variable")
    exit(1)

# Webhook configuration
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Must be set for webhook to work

bot = Bot(TOKEN)

@bot.command(r"start")
async def start(event):
    """Welcome message for webhook bot."""
    welcome_text = """
🌐 *Webhook Bot*

I'm running on webhooks instead of polling! This is more efficient for production.

*Features:*
• Webhook-based updates (no polling)
• HTTPS support
• Automatic SSL handling
• Production-ready

*Commands:*
/start - This welcome message
/info - Bot information
/webhook_status - Webhook status
/help - Help information

*Webhook Details:*
• Host: `{WEBHOOK_HOST}`
• Port: `{WEBHOOK_PORT}`
• Path: `{WEBHOOK_PATH}`
• URL: `{WEBHOOK_URL or 'Not set'}`
"""
    await event.send_message(
        welcome_text.format(
            WEBHOOK_HOST=WEBHOOK_HOST,
            WEBHOOK_PORT=WEBHOOK_PORT,
            WEBHOOK_PATH=WEBHOOK_PATH,
            WEBHOOK_URL=WEBHOOK_URL
        ),
        parse_mode="Markdown"
    )

@bot.command(r"info")
async def info(event):
    """Show bot information."""
    info_text = f"""
🤖 *Bot Information*

• **Framework:** Gpgram v1.0.0
• **Update Method:** Webhook
• **Python Version:** 3.12+
• **User ID:** `{event.user_id}`
• **Chat ID:** `{event.chat_id}`
• **Chat Type:** `{event.chat_type or 'Unknown'}`

*Webhook Configuration:*
• Host: `{WEBHOOK_HOST}:{WEBHOOK_PORT}`
• Path: `{WEBHOOK_PATH}`
• SSL: Enabled
"""
    await event.send_message(info_text, parse_mode="Markdown")

@bot.command(r"webhook_status")
async def webhook_status(event):
    """Show webhook status."""
    try:
        # Get webhook info from Telegram
        webhook_info = await bot.get_webhook_info()

        if webhook_info:
            status_text = f"""
🔗 *Webhook Status*

• **URL:** `{webhook_info.get('url', 'Not set')}`
• **Has Custom Certificate:** `{webhook_info.get('has_custom_certificate', False)}`
• **Pending Updates:** `{webhook_info.get('pending_update_count', 0)}`
• **Max Connections:** `{webhook_info.get('max_connections', 'Unknown')}`
• **IP Address:** `{webhook_info.get('ip_address', 'Not set')}`

*Last Error:*
```
{webhook_info.get('last_error_message', 'No errors')}
```

*Last Error Date:* `{webhook_info.get('last_error_date', 'Never')}`
"""
        else:
            status_text = "❌ Unable to retrieve webhook status"

    except Exception as e:
        status_text = f"❌ Error getting webhook status: `{str(e)}`"

    await event.send_message(status_text, parse_mode="Markdown")

@bot.command(r"help")
async def help_command(event):
    """Show help information."""
    help_text = """
📚 *Webhook Bot Help*

This bot demonstrates webhook functionality in Gpgram.

*Setting up Webhooks:*

1. **Get SSL Certificate:**
   ```bash
   # Generate self-signed certificate for testing
   openssl req -newkey rsa:2048 -sha256 -nodes \\
     -keyout private.key -x509 -days 365 -out public.pem \\
     -subj "/C=US/ST=State/L=City/O=Organization/CN=yourdomain.com"
   ```

2. **Set Environment Variables:**
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   export WEBHOOK_HOST="0.0.0.0"
   export WEBHOOK_PORT="8443"
   export WEBHOOK_URL="https://yourdomain.com/webhook"
   ```

3. **Run the Bot:**
   ```bash
   python webhook_bot.py
   ```

*Webhook Advantages:*
• ✅ No polling required
• ✅ Instant updates
• ✅ Lower server load
• ✅ Better for production
• ✅ Supports SSL/TLS

*Commands:*
/start - Welcome message
/info - Bot information
/webhook_status - Webhook status
/help - This help

*Note:* Webhooks require HTTPS in production!
"""
    await event.send_message(help_text, parse_mode="Markdown")

@bot.on_message(r"^(?!/).+")  # Match any non-command message
async def echo_message(event):
    """Echo back any message (excluding commands)."""
    await event.reply(f"📡 Webhook received: {event.text}")

async def setup_webhook():
    """Set up webhook with Telegram."""
    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL environment variable not set!")
        print("Please set it to your webhook URL (e.g., https://yourdomain.com/webhook)")
        return False

    try:
        print(f"🔗 Setting up webhook at: {WEBHOOK_URL}")

        # Set webhook with Telegram
        success = await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True
        )

        if success:
            print("✅ Webhook set up successfully!")
            return True
        else:
            print("❌ Failed to set up webhook")
            return False

    except Exception as e:
        print(f"❌ Error setting up webhook: {e}")
        return False

async def main():
    """Main function to run the webhook bot."""
    print("🚀 Starting Webhook Bot...")
    print(f"Host: {WEBHOOK_HOST}:{WEBHOOK_PORT}")
    print(f"Path: {WEBHOOK_PATH}")
    print(f"URL: {WEBHOOK_URL or 'Not configured'}")

    # Set up webhook first
    webhook_ok = await setup_webhook()
    if not webhook_ok:
        print("❌ Webhook setup failed. Exiting.")
        return

    # Import webhook server
    from gpgram.api.webhook import WebhookServer

    # Create webhook server
    server = WebhookServer(
        dispatcher=None,  # We'll handle updates directly
        host=WEBHOOK_HOST,
        port=WEBHOOK_PORT,
        webhook_path=WEBHOOK_PATH,
        secret_token=None  # Add a secret token in production
    )

    # Add custom route to handle webhook updates
    async def handle_webhook(request):
        """Handle incoming webhook updates."""
        try:
            update_data = await request.json()
            print(f"📨 Received update: {update_data}")

            # Process the update with our bot
            await bot.process_update(update_data)

            return web.Response(status=200, text="OK")

        except Exception as e:
            print(f"❌ Error processing webhook: {e}")
            return web.Response(status=500, text="Internal Server Error")

    # Add the webhook route
    server.app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Add health check route
    async def health_check(request):
        return web.Response(status=200, text="OK")

    server.app.router.add_get("/health", health_check)

    try:
        print("🌐 Starting webhook server...")
        await server.start()

        print("✅ Webhook bot is running!")
        print(f"📡 Listening on {WEBHOOK_HOST}:{WEBHOOK_PORT}")
        print("💡 Send messages to your bot to test webhook functionality")

        # Keep the server running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        # Clean up
        await bot.close()
        await server.stop()

if __name__ == "__main__":
    # Check if aiohttp is available for webhook server
    try:
        from aiohttp import web
        asyncio.run(main())
    except ImportError:
        print("❌ aiohttp is required for webhook functionality")
        print("Install it with: pip install aiohttp")
        exit(1)