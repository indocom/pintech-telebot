from typing import Optional, Set

from telegram import Update
from telegram.ext import (
    CallbackContext,
    Dispatcher,
)


class CustomContext(CallbackContext[dict, ChatData, dict]):
    """Custom class for context.
    Reference: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/contexttypesbot.py
    """

    def __init__(self, dispatcher: Dispatcher):
        super().__init__(dispatcher=dispatcher)
        self._message_id: Optional[int] = None

    @property
    def bot_user_ids(self) -> Set[int]:
        """Custom shortcut to access a value stored in the bot_data dict"""
        return self.bot_data.setdefault('user_ids', set())

    @property
    def message_clicks(self) -> Optional[int]:
        """Access the number of clicks for the message this context object was built for."""
        if self._message_id:
            return self.chat_data.clicks_per_message[self._message_id]
        return None

    @message_clicks.setter
    def message_clicks(self, value: int) -> None:
        """Allow to change the count"""
        if not self._message_id:
            raise RuntimeError('There is no message associated with this context obejct.')
        self.chat_data.clicks_per_message[self._message_id] = value

    @classmethod
    def from_update(cls, update: object, dispatcher: Dispatcher) -> CallbackContext:
        """Override from_update to set _message_id."""
        # Make sure to call super()
        context = super().from_update(update, dispatcher)

        if context.chat_data and isinstance(update, Update) and update.effective_message:
            context._message_id = update.effective_message.message_id  # pylint: disable=W0212

        # Remember to return the object
        return context
