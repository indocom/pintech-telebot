from abc import ABC, abstractmethod
from typing import Callable

from telegram.ext import CallbackContext


class BaseJob(ABC):
    """
    Base Class for Job, job will be running at certain interval
    """

    @property
    @abstractmethod
    def help_message(self):
        pass

    @abstractmethod
    def get_job(self) -> Callable[[CallbackContext], None]:
        pass

    @property
    @abstractmethod
    def interval(self):
        """
        The interval in second when the job is scheduled to run
        """
        pass
