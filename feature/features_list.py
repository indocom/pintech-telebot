from feature.github.broadcast_pr_job import BroadcastPrJob
from feature.github.get_repo_list import GetRepoCommand
from feature.github.get_subscribed_repo import GetSubscribedRepoCommand
from feature.github.subscribe_repo import SubscribeRepoCommand
from feature.github.unsubscribe_repo import UnsubscribeRepoCommand
from feature.kudo.reply_kudo_message import ReplyKudoMessage

COMMANDS = [
    GetRepoCommand(),
    GetSubscribedRepoCommand(),
    SubscribeRepoCommand(),
    UnsubscribeRepoCommand(),
    ReplyKudoMessage(),
]

JOBS = [
    BroadcastPrJob()
]
