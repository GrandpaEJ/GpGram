"""
User type for Telegram API.
"""

from .base import TelegramObject


class User(TelegramObject):
    """
    This object represents a Telegram user or bot.

    Attributes:
        id: Unique identifier for this user or bot
        is_bot: True, if this user is a bot
        first_name: User's or bot's first name
        last_name: User's or bot's last name
        username: User's or bot's username
        language_code: IETF language tag of the user's language
        is_premium: True, if this user is a Telegram Premium user
        added_to_attachment_menu: True, if this user added the bot to the attachment menu
        can_join_groups: True, if the bot can be invited to groups
        can_read_all_group_messages: True, if privacy mode is disabled for the bot
        supports_inline_queries: True, if the bot supports inline queries
    """

    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    can_join_groups: bool | None = None
    can_read_all_group_messages: bool | None = None
    supports_inline_queries: bool | None = None

    @property
    def full_name(self) -> str:
        """
        Get the user's full name.

        Returns:
            The user's full name (first name + last name if available)
        """
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def mention(self) -> str:
        """
        Get a Markdown mention of the user.

        Returns:
            A Markdown mention of the user
        """
        return f"[{self.full_name}](tg://user?id={self.id})"
