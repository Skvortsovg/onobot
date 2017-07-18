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

from menu import BaseState as State
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


def button(bot, update):
    if update.callback_query.data == 'More':
        headers = get_other_hot_news()
        bot.editMessageReplyMarkup(chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id, reply_markup='')
        bot.sendMessage(chat_id=update.callback_query.message.chat.id, text = headers, reply_markup=keyboard, parse_mode='html',
            disable_web_page_preview=1)
    else:
        bot.editMessageReplyMarkup(chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id, reply_markup='')


updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, State))
updater.dispatcher.add_handler(CommandHandler('start', State))
updater.dispatcher.add_error_handler(error)

job_queue = updater.job_queue
job_queue.put(Job(update_all, 7200.0), next_t=0.0)

