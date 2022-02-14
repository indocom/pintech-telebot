from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Base Class for Commands, which is the core class of feature in pinus telebot currently.
    """

    @property
    @abstractmethod
    def help_message(self):
        pass

    @property
    @abstractmethod
    def handler(self):
        pass
