# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

import re
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    Job,
)
from settings import *
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from menu import BaseState as State, callback_query_handler
from utils import upd_news, update_clusters, set_hot_news, get_other_hot_news

log = logging.getLogger(__name__)


def error(bot, update, error):
    log.error('Update: %(update)r caused an error:' % vars())
    log.exception(error)


def update_all(bot, update):
    upd_news()
    for category in ['Kremlin', 'Megafon']:
        update_clusters(category)
        set_hot_news(category)

# from utils import send_async_message, edit_async_message_markup
# from utils import langs

# keyboard = telegram.ReplyKeyboardMarkup([[_('NEW_BUTTON'), _('MAIN_BUTTON'), _('CUBES_BUTTON')]], resize_keyboard=1)


updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, State))
updater.dispatcher.add_handler(CommandHandler('start', State))
updater.dispatcher.add_error_handler(error)
updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

job_queue = updater.job_queue
job_queue.put(Job(update_all, 7200.0), next_t=3600.0)

