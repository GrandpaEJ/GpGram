"""
Chat type for Telegram API.
"""

from typing import TYPE_CHECKING, Any, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from .message import Message


class Chat(TelegramObject):
    """
    This object represents a chat.

    Attributes:
        id: Unique identifier for this chat
        type: Type of chat, can be either "private", "group", "supergroup" or "channel"
        title: Title, for supergroups, channels and group chats
        username: Username, for private chats, supergroups and channels if available
        first_name: First name of the other party in a private chat
        last_name: Last name of the other party in a private chat
        photo: Chat photo
        bio: Bio of the other party in a private chat
        description: Description, for groups, supergroups and channel chats
        invite_link: Primary invite link, for groups, supergroups and channel chats
        pinned_message: The most recent pinned message
        permissions: Default chat member permissions, for groups and supergroups
        slow_mode_delay: For supergroups, the minimum allowed delay between consecutive messages
        message_auto_delete_time: The time after which all messages will be automatically deleted
        has_protected_content: True, if messages from the chat can't be forwarded to other chats
        sticker_set_name: For supergroups, name of group sticker set
        can_set_sticker_set: True, if the bot can change the group sticker set
        linked_chat_id: Unique identifier for the linked chat
        location: For supergroups, the location to which the supergroup is connected
    """

    id: int
    type: str
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    photo: dict[str, Any] | None = None
    bio: str | None = None
    description: str | None = None
    invite_link: str | None = None
    pinned_message: Optional["Message"] = None  # type: ignore
    permissions: dict[str, Any] | None = None
    slow_mode_delay: int | None = None
    message_auto_delete_time: int | None = None
    has_protected_content: bool | None = None
    sticker_set_name: str | None = None
    can_set_sticker_set: bool | None = None
    linked_chat_id: int | None = None
    location: dict[str, Any] | None = None

    @property
    def full_name(self) -> str:
        """
        Get the chat's full name.

        Returns:
            The chat's full name (title for groups, first name + last name for private chats)
        """
        if self.type == "private":
            if self.last_name:
                return f"{self.first_name} {self.last_name}"
            return self.first_name or ""
        return self.title or ""

    @property
    def is_private(self) -> bool:
        """Check if the chat is a private chat."""
        return self.type == "private"

    @property
    def is_group(self) -> bool:
        """Check if the chat is a group chat."""
        return self.type == "group"

    @property
    def is_supergroup(self) -> bool:
        """Check if the chat is a supergroup."""
        return self.type == "supergroup"

    @property
    def is_channel(self) -> bool:
        """Check if the chat is a channel."""
        return self.type == "channel"
