"""
Gpgram - A modern, clean Telegram Bot API library.
"""

import asyncio
import re
from collections.abc import Awaitable, Callable
from typing import Any

import httpx

from .types.callback_query import CallbackQuery
from .types.message import Message
from .types.update import Update


class Bot:
    """
    A clean and simple Telegram Bot API client.

    This class provides a straightforward interface for building Telegram bots
    with event-driven programming and decorator-based handlers.
    """

    def __init__(
        self,
        token: str,
        timeout: float = 30.0,
        api_url: str | None = None,
    ):
        """
        Initialize the bot.

        Args:
            token: Telegram bot token
            timeout: Request timeout in seconds
            api_url: Custom API URL (optional)
        """
        self.token = token
        self.timeout = timeout
        self.api_url = api_url or f"https://api.telegram.org/bot{token}"

        # HTTP client with connection pooling
        self._client = httpx.AsyncClient(
            timeout=timeout,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=100),
        )

        # Event handlers
        self._handlers: list[Callable] = []
        self._command_handlers: dict[str, list[Callable]] = {}
        self._message_handlers: list[Callable] = []
        self._callback_handlers: list[Callable] = []

        # Running state
        self._running = False
        self._polling_task: asyncio.Task | None = None
        self._offset: int | None = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the bot and cleanup resources."""
        self._running = False
        if self._polling_task:
            self._polling_task.cancel()
            try:
                await self._polling_task
            except asyncio.CancelledError:
                pass
        await self._client.aclose()

    async def _make_request(self, method: str, **params) -> dict[str, Any]:
        """
        Make a request to the Telegram API.

        Args:
            method: API method name
            **params: Method parameters

        Returns:
            API response data
        """
        url = f"{self.api_url}/{method}"

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        for attempt in range(3):
            try:
                response = await self._client.post(url, json=params)
                response.raise_for_status()
                data = response.json()

                if not data.get("ok"):
                    raise Exception(
                        f"API Error: {data.get('description', 'Unknown error')}"
                    )

                return data["result"]

            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(0.5 * (2**attempt))

    def command(self, pattern: str | None = None):
        """
        Decorator to register a command handler.

        Args:
            pattern: Regex pattern for command matching. If None, matches all commands.

        Returns:
            Decorator function
        """

        def decorator(func: Callable[["Event"], Awaitable[None]]) -> Callable:
            if pattern is None:
                # Match all commands
                self._handlers.append(func)
            else:
                # Compile regex pattern
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                self._command_handlers[pattern] = self._command_handlers.get(
                    pattern, []
                ) + [func]
                # Store pattern for later use
                func._pattern = compiled_pattern
            return func

        return decorator

    def on_message(self, pattern: str | None = None):
        """
        Decorator to register a message handler.

        Args:
            pattern: Regex pattern for message matching. If None, matches all messages.

        Returns:
            Decorator function
        """

        def decorator(func: Callable[["Event"], Awaitable[None]]) -> Callable:
            if pattern is None:
                self._message_handlers.append(func)
            else:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                func._pattern = compiled_pattern
                self._message_handlers.append(func)
            return func

        return decorator

    def on_callback(self, pattern: str | None = None):
        """
        Decorator to register a callback query handler.

        Args:
            pattern: Regex pattern for callback data matching. If None, matches all callbacks.

        Returns:
            Decorator function
        """

        def decorator(func: Callable[["Event"], Awaitable[None]]) -> Callable:
            if pattern is None:
                self._callback_handlers.append(func)
            else:
                compiled_pattern = re.compile(pattern, re.IGNORECASE)
                func._pattern = compiled_pattern
                self._callback_handlers.append(func)
            return func

        return decorator

    async def _process_update(self, update_data: dict[str, Any]) -> None:
        """
        Process a single update.

        Args:
            update_data: Update data from Telegram
        """
        update = Update.from_dict(update_data)
        event = Event(update, self)

        # Handle messages
        if update.message:
            await self._handle_message(event)

        # Handle callback queries
        elif update.callback_query:
            await self._handle_callback(event)

    async def _handle_message(self, event: "Event") -> None:
        """
        Handle message events.

        Args:
            event: Event object
        """
        text = event.text or ""

        # Check command handlers first
        if text.startswith("/"):
            # Check specific command patterns
            for _pattern, handlers in self._command_handlers.items():
                if hasattr(handlers[0], "_pattern") and handlers[0]._pattern.search(
                    text
                ):
                    for handler in handlers:
                        await handler(event)
                    return

            # Check general command handlers
            for handler in self._handlers:
                await handler(event)
            return

        # Handle regular messages
        for handler in self._message_handlers:
            if not hasattr(handler, "_pattern") or handler._pattern.search(text):
                await handler(event)

    async def _handle_callback(self, event: "Event") -> None:
        """
        Handle callback query events.

        Args:
            event: Event object
        """
        data = event.callback_data or ""

        for handler in self._callback_handlers:
            if not hasattr(handler, "_pattern") or handler._pattern.search(data):
                await handler(event)

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        parse_mode: str | None = None,
        reply_markup: dict[str, Any] | None = None,
        **kwargs,
    ) -> Message:
        """
        Send a text message.

        Args:
            chat_id: Chat ID to send to
            text: Message text
            parse_mode: Parse mode (Markdown, HTML, etc.)
            reply_markup: Reply markup
            **kwargs: Additional parameters

        Returns:
            Sent message
        """
        result = await self._make_request(
            "sendMessage",
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            **kwargs,
        )
        return Message.from_dict(result)

    async def edit_message_text(
        self,
        text: str,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: str | None = None,
        reply_markup: dict[str, Any] | None = None,
        **kwargs,
    ) -> Message | bool:
        """
        Edit a message text.

        Args:
            text: New text
            chat_id: Chat ID
            message_id: Message ID to edit
            inline_message_id: Inline message ID
            parse_mode: Parse mode
            reply_markup: Reply markup
            **kwargs: Additional parameters

        Returns:
            Edited message or True for inline messages
        """
        result = await self._make_request(
            "editMessageText",
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            **kwargs,
        )

        if isinstance(result, bool):
            return result
        return Message.from_dict(result)

    async def delete_message(self, chat_id: int | str, message_id: int) -> bool:
        """
        Delete a message.

        Args:
            chat_id: Chat ID
            message_id: Message ID to delete

        Returns:
            True on success
        """
        await self._make_request(
            "deleteMessage", chat_id=chat_id, message_id=message_id
        )
        return True

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool | None = None,
        **kwargs,
    ) -> bool:
        """
        Answer a callback query.

        Args:
            callback_query_id: Callback query ID
            text: Notification text
            show_alert: Whether to show alert
            **kwargs: Additional parameters

        Returns:
            True on success
        """
        await self._make_request(
            "answerCallbackQuery",
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            **kwargs,
        )
        return True

    async def polling(
        self,
        interval: float = 0.5,
        timeout: int = 30,
        drop_pending_updates: bool = False,
    ) -> None:
        """
        Start polling for updates.

        Args:
            interval: Polling interval in seconds
            timeout: Long polling timeout
            drop_pending_updates: Whether to drop pending updates
        """
        if drop_pending_updates:
            self._offset = -1
            await self._make_request("getUpdates", offset=-1, limit=1, timeout=0)

        self._running = True

        while self._running:
            try:
                updates = await self._make_request(
                    "getUpdates",
                    offset=self._offset,
                    timeout=timeout,
                    allowed_updates=["message", "callback_query"],
                )

                for update_data in updates:
                    await self._process_update(update_data)
                    self._offset = update_data["update_id"] + 1

            except Exception as e:
                print(f"Polling error: {e}")
                await asyncio.sleep(interval)

    def run(self) -> None:
        """
        Run the bot (blocking).
        """
        asyncio.run(self.polling())


class Event:
    """
    Event wrapper for Telegram updates.
    """

    def __init__(self, update: Update, bot: Bot):
        """
        Initialize an event.

        Args:
            update: Telegram update
            bot: Bot instance
        """
        self.update = update
        self.bot = bot

    @property
    def message(self) -> Message | None:
        """Get the message from the event."""
        return self.update.message

    @property
    def callback_query(self) -> CallbackQuery | None:
        """Get the callback query from the event."""
        return self.update.callback_query

    @property
    def text(self) -> str | None:
        """Get the text from the event."""
        if self.message:
            return self.message.text
        return None

    @property
    def photo(self) -> list[dict[str, Any]] | None:
        """Get the photo from the event."""
        if self.message:
            return self.message.photo
        return None

    @property
    def document(self) -> dict[str, Any] | None:
        """Get the document from the event."""
        if self.message:
            return self.message.document
        return None

    @property
    def audio(self) -> dict[str, Any] | None:
        """Get the audio from the event."""
        if self.message:
            return self.message.audio
        return None

    @property
    def video(self) -> dict[str, Any] | None:
        """Get the video from the event."""
        if self.message:
            return self.message.video
        return None

    @property
    def animation(self) -> dict[str, Any] | None:
        """Get the animation from the event."""
        if self.message:
            return self.message.animation
        return None

    @property
    def sticker(self) -> dict[str, Any] | None:
        """Get the sticker from the event."""
        if self.message:
            return self.message.sticker
        return None

    @property
    def voice(self) -> dict[str, Any] | None:
        """Get the voice from the event."""
        if self.message:
            return self.message.voice
        return None

    @property
    def callback_data(self) -> str | None:
        """Get the callback data from the event."""
        if self.callback_query:
            return self.callback_query.data
        return None

    @property
    def chat_id(self) -> int | None:
        """Get the chat ID from the event."""
        if self.message:
            return self.message.chat.id
        elif self.callback_query and self.callback_query.message:
            return self.callback_query.message.chat.id
        return None

    @property
    def user_id(self) -> int | None:
        """Get the user ID from the event."""
        if self.message and self.message.from_user:
            return self.message.from_user.id
        elif self.callback_query and self.callback_query.from_user:
            return self.callback_query.from_user.id
        return None

    async def send_message(self, text: str | None = None, **kwargs) -> Message:
        """
        Send a message in response to this event.

        Args:
            text: Message text (optional when sending media)
            **kwargs: Additional parameters

        Returns:
            Sent message
        """
        if not self.chat_id:
            raise ValueError("No chat ID available for this event")

        # Handle the case where text is passed as a kwarg (e.g., from reply method)
        if text is None and 'text' in kwargs:
            text = kwargs.pop('text')

        # Handle media-specific parameters
        media_keys = ['photo', 'document', 'audio', 'video', 'animation', 'sticker', 'voice']
        media_type = next((key for key in media_keys if key in kwargs), None)

        if media_type:
            # For media messages, use the core bot's send methods
            method_name = f'send_{media_type}'
            if hasattr(self.bot, method_name):
                method = getattr(self.bot, method_name)
                # Extract media-specific params
                allowed_keys = ['caption', 'parse_mode', 'reply_markup', 'disable_notification',
                              'protect_content', 'reply_to_message_id', 'allow_sending_without_reply',
                              'thumb', 'title', 'performer', 'duration', 'width', 'height',
                              'disable_content_type_detection']
                media_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys or k == media_type}
                media_kwargs['chat_id'] = self.chat_id
                result = await method(**media_kwargs)
                # Ensure we return a Message object
                if isinstance(result, dict):
                    return Message.from_dict(result)
                elif hasattr(result, '__dict__'):
                    return result
                else:
                    # If result is not a dict or Message, something went wrong
                    raise ValueError(f"Unexpected result type from {method_name}: {type(result)}")
            else:
                # Fallback to send_message if method doesn't exist
                if text is None:
                    raise ValueError("Event.send_message() requires 'text' parameter when not sending media")
                return await self.bot.send_message(self.chat_id, text, **kwargs)
        else:
            if text is None:
                raise ValueError("Event.send_message() requires 'text' parameter when not sending media")
            return await self.bot.send_message(self.chat_id, text, **kwargs)

    async def reply(self, text: str, **kwargs) -> Message:
        """
        Reply to this event.

        Args:
            text: Message text
            **kwargs: Additional parameters

        Returns:
            Sent message
        """
        if not self.chat_id:
            raise ValueError("No chat ID available for this event")

        message_id = None
        if self.message:
            message_id = self.message.message_id

        return await self.send_message(text, reply_to_message_id=message_id, **kwargs)

    async def edit_message(self, text: str, **kwargs) -> Message | bool:
        """
        Edit the message in this event.

        Args:
            text: New text
            **kwargs: Additional parameters

        Returns:
            Edited message
        """
        if not self.message:
            raise ValueError("No message available to edit")

        return await self.bot.edit_message_text(
            text, chat_id=self.chat_id, message_id=self.message.message_id, **kwargs
        )

    async def delete_message(self) -> bool:
        """
        Delete the message in this event.

        Returns:
            True on success
        """
        if not self.message:
            raise ValueError("No message available to delete")

        return await self.bot.delete_message(self.chat_id, self.message.message_id)

    async def answer_callback(self, text: str | None = None, **kwargs) -> bool:
        """
        Answer the callback query in this event.

        Args:
            text: Notification text
            **kwargs: Additional parameters

        Returns:
            True on success
        """
        if not self.callback_query:
            raise ValueError("No callback query available to answer")

        return await self.bot.answer_callback_query(
            self.callback_query.id, text=text, **kwargs
        )
