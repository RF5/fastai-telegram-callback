# pip requirements:
# fastai
# python-telegram-bot

from telegram.ext import Updater
from fastai.train import Learner, LearnerCallback
from fastai.metrics import MetricsList
from fastai.core import ifnone
from torch import Tensor
from time import time
from fastprogress.fastprogress import format_time
from warnings import warn

class TelegramNotifier(LearnerCallback):
    "A `LearnerCallback` that notifies you via telegram when an epoch is done, and its associated metrics."
    def __init__(self, learn:Learner, chat_id:int=None, token:str=None): 
        super().__init__(learn)
        if token is None:
            raise ValueError("Please supply your bot token")
        if chat_id is None:
            raise ValueError("Please supply the chat id you wish to send the notifications to")
        self.updater = Updater(token=token)
        self.chat_id = chat_id
        self.bot = self.updater.bot 
        self.add_time = True

    def on_epoch_begin(self, **kwargs)->None:
        if self.add_time: self.start_epoch = time()
        
    def on_epoch_end(self, epoch: int, smooth_loss: Tensor, last_metrics: MetricsList, **kwargs) -> bool:
        "Add a line with `epoch` number, `smooth_loss` and `last_metrics`."
        msg = ','.join(self.learn.recorder.names[:(None if self.add_time else -1)]) + '\n'
        last_metrics = ifnone(last_metrics, [])
        stats = [str(stat) if isinstance(stat, int) else '#na#' if stat is None else f'{stat:.6f}'
                 for name, stat in zip(self.learn.recorder.names, [epoch, smooth_loss] + last_metrics)]
        if self.add_time: stats.append(format_time(time() - self.start_epoch))
        str_stats = ','.join(stats)
        msg = msg + str_stats + '\n'
        
        try:
            self.bot.send_message(chat_id=self.chat_id, text=msg)
        except Exception as e:
            warn("Could not deliver message. Error: " + str(e), RuntimeWarning)
        
