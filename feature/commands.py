from feature.get_repo_list import GetRepoCommand
from feature.get_subscribed_repo import GetSubscribedRepoCommand
from feature.subscribe_repo import SubscribeRepoCommand
from feature.unsubscribe_repo import UnsubscribeRepoCommand

COMMANDS = [
    SubscribeRepoCommand(),
    UnsubscribeRepoCommand(),
    GetRepoCommand(),
    GetSubscribedRepoCommand(),
]
