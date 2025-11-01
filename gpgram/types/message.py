"""
Message type for Telegram API.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

if TYPE_CHECKING:
    from ..bot import Bot

from .base import TelegramObject
from .chat import Chat
from .user import User


class Message(TelegramObject):
    """
    This object represents a message.

    Attributes:
        message_id: Unique message identifier inside this chat
        from_user: Sender of the message; empty for messages sent to channels
        date: Date the message was sent
        chat: Conversation the message belongs to
        text: For text messages, the actual UTF-8 text of the message
        # ... many more attributes as per Telegram API
    """

    message_id: int
    date: datetime
    chat: "Chat"
    from_user: Optional["User"] = Field(None, alias="from")
    text: str | None = None
    entities: list[dict[str, Any]] | None = None
    animation: dict[str, Any] | None = None
    audio: dict[str, Any] | None = None
    document: dict[str, Any] | None = None
    photo: list[dict[str, Any]] | None = None
    sticker: dict[str, Any] | None = None
    video: dict[str, Any] | None = None
    video_note: dict[str, Any] | None = None
    voice: dict[str, Any] | None = None
    caption: str | None = None
    caption_entities: list[dict[str, Any]] | None = None
    contact: dict[str, Any] | None = None
    dice: dict[str, Any] | None = None
    game: dict[str, Any] | None = None
    poll: dict[str, Any] | None = None
    venue: dict[str, Any] | None = None
    location: dict[str, Any] | None = None
    new_chat_members: list[dict[str, Any]] | None = None
    left_chat_member: dict[str, Any] | None = None
    new_chat_title: str | None = None
    new_chat_photo: list[dict[str, Any]] | None = None
    delete_chat_photo: bool | None = None
    group_chat_created: bool | None = None
    supergroup_chat_created: bool | None = None
    channel_chat_created: bool | None = None
    message_auto_delete_timer_changed: dict[str, Any] | None = None
    migrate_to_chat_id: int | None = None
    migrate_from_chat_id: int | None = None
    pinned_message: Optional["Message"] = None
    invoice: dict[str, Any] | None = None
    successful_payment: dict[str, Any] | None = None
    connected_website: str | None = None
    passport_data: dict[str, Any] | None = None
    proximity_alert_triggered: dict[str, Any] | None = None
    voice_chat_scheduled: dict[str, Any] | None = None
    voice_chat_started: dict[str, Any] | None = None
    voice_chat_ended: dict[str, Any] | None = None
    voice_chat_participants_invited: dict[str, Any] | None = None
    reply_to_message: Optional["Message"] = None
    via_bot: User | None = None
    forward_from: User | None = None
    forward_from_chat: Chat | None = None
    forward_from_message_id: int | None = None
    forward_signature: str | None = None
    forward_sender_name: str | None = None
    forward_date: datetime | None = None
    is_automatic_forward: bool | None = None
    reply_markup: dict[str, Any] | None = None

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}

    async def reply(
        self,
        bot: "Bot",
        text: str,
        parse_mode: str | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        reply_markup: dict[str, Any] | None = None,
    ) -> "Message":
        """
        Reply to this message with text.

        Args:
            bot: Bot instance to use for sending the message
            text: Text of the message to be sent
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
            reply_markup: Additional interface options

        Returns:
            The sent Message
        """
        return await bot.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id,
            reply_markup=reply_markup,
        )

    async def edit_text(
        self,
        bot: "Bot",
        text: str,
        parse_mode: str | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any] | bool:
        """
        Edit this message's text.

        Args:
            bot: Bot instance to use for editing the message
            text: New text of the message
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            reply_markup: Additional interface options

        Returns:
            The edited Message or True on success
        """
        return await bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.message_id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )

    async def delete(self, bot: "Bot") -> bool:
        """
        Delete this message.

        Args:
            bot: Bot instance to use for deleting the message

        Returns:
            True on success
        """
        return await bot.delete_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    @property
    def is_command(self) -> bool:
        """Check if the message is a command."""
        return bool(self.text and self.text.startswith("/"))

    @property
    def command(self) -> str | None:
        """Get the command without the slash."""
        if not self.is_command:
            return None

        command_parts = self.text.split()
        if not command_parts:
            return None

        # Remove the slash and extract command name
        command = command_parts[0][1:].split("@")[0]
        return command

    @property
    def args(self) -> list[str]:
        """Get the command arguments."""
        if not self.is_command or not self.text:
            return []

        command_parts = self.text.split()
        if len(command_parts) <= 1:
            return []

        return command_parts[1:]

    def get_command(self) -> str | None:
        """Get the command name (alias for command property)."""
        return self.command

    def get_args(self) -> list[str]:
        """Get the command arguments (alias for args property)."""
        return self.args
