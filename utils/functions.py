# -*- coding: utf-8 -*-


from .decorators import async
import time
import logging

log = logging.getLogger(__name__)


MAX_RETRIES = 5
WAIT_TIME = 0.5
#@async
#def send_async_message(bot, update, text, markup=None, parse_mode=None):
#
#    bot.sendMessage(
#        update.message.chat_id,
#        text=text,
#        reply_markup=markup,
#        parse_mode=parse_mode,
#    )
#
#
#@async
#def send_async_location(bot, update, latitude=0, longitude=0, markup=None):
#
#    bot.sendLocation(
#        update.message.chat_id,
#        latitude=latitude,
#        longitude=longitude,
#        reply_markup=markup,
#    )
#
#
#@async
#def edit_async_message(bot, update, text, markup=None, parse_mode=None, disable_web_page_preview=True):
#    query = update.callback_query
#
#    bot.editMessageText(
#        chat_id=query.message.chat_id,
#        message_id=query.message.message_id,
#        text=text,
#        reply_markup=markup,
#        parse_mode=parse_mode,
#        disable_web_page_preview=disable_web_page_preview,
#    )
import types

@async
def send_async_message(bot, update, text, markup=None, parse_mode=None, disable_web_page_preview=True, disable_notification=False):
    retries_left = MAX_RETRIES
    try:
        chat_id = update.message.chat_id
    except Exception:
        chat_id = int(update)

    log.info('Sending message to %(chat_id)d' % dict(chat_id=chat_id))

    while retries_left > 0:

        try:
            bot.sendMessage(
                chat_id=chat_id,
                text=text,
                reply_markup=markup,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
            )

        except Exception as err:
            log.exception(err)
            retries_left -= 1
            if retries_left < 1:
                log.critical('Failed to send message to %(chat_id)d' % dict(chat_id=chat_id))
                return

            log.warning(
                'Failed attempt to send message [%(cn)d/%(tn)d] '
                'to %(chat_id)d. Will try again via '
                '%(num).2f seconds' % dict(
                    chat_id=chat_id,
                    num=WAIT_TIME,
                    tn=MAX_RETRIES,
                    cn=retries_left,
                )
            )
            time.sleep(WAIT_TIME)

        else:
            return


@async
def send_async_location(bot, update, latitude=0.0, longitude=0.0, markup=None, disable_notification=False):

    if update.message is None:
        log.error('function send_async_location: `update.message` is None')
        return

    retries_left = MAX_RETRIES

    chat_id = update.message.chat_id

    log.info('Sending message to %(chat_id)d' % dict(chat_id=chat_id))

    while retries_left > 0:

        try:
            bot.sendLocation(
                chat_id=chat_id,
                latitude=latitude,
                longitude=longitude,
                reply_markup=markup,
                disable_notification=disable_notification,
            )

        except Exception as err:
            log.exception(err)
            retries_left -= 1
            if retries_left < 1:
                log.critical('Failed to send message to %(chat_id)d' % dict(chat_id=chat_id))
                return

            log.warning(
                'Failed attempt to send message [%(cn)d/%(tn)d] '
                'to %(chat_id)d. Will try again via '
                '%(num).2f seconds' % dict(
                    chat_id=chat_id,
                    num=WAIT_TIME,
                    tn=MAX_RETRIES,
                    cn=retries_left,
                )
            )
            time.sleep(WAIT_TIME)

        else:
            return


@async
def edit_async_message(bot, update, text, markup=None, parse_mode=None, disable_web_page_preview=True):
    query = update.callback_query

    if query.message is None:
        log.error('function edit_async_message: `query.message` is None')
        return

    retries_left = MAX_RETRIES

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    log.info('Sending message edit to %(chat_id)d:%(message_id)d' % dict(
        chat_id=chat_id,
        message_id=message_id,
    ))

    while retries_left > 0:

        try:
            bot.editMessageText(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=markup,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
            )

        except Exception as err:
            log.exception(err)
            retries_left -= 1
            if retries_left < 1:
                log.critical('Failed to send message to %(chat_id)d' % dict(chat_id=chat_id))
                return

            log.warning(
                'Failed attempt to send message [%(cn)d/%(tn)d] '
                'to %(chat_id)d. Will try again via '
                '%(num).2f seconds' % dict(
                    chat_id=chat_id,
                    num=WAIT_TIME,
                    tn=MAX_RETRIES,
                    cn=retries_left,
                )
            )
            time.sleep(WAIT_TIME)

        else:
            return

@async
def edit_async_message_markup(bot, update, markup=None):
    query = update.callback_query

    if query.message is None:
        log.error('function edit_async_markup: `query.message` is None')
        return

    retries_left = MAX_RETRIES

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    log.info('Sending message to %(chat_id)d:%(message_id)d' % dict(
        chat_id=chat_id,
        message_id=message_id,
    ))

    while retries_left > 0:

        try:
            bot.editMessageReplyMarkup(
                chat_id=chat_id,
                message_id=query.message.message_id,
                reply_markup=markup,
            )

        except Exception as err:
            log.exception(err)
            retries_left -= 1
            if retries_left < 1:
                log.critical('Failed to send message to %(chat_id)d' % dict(chat_id=chat_id))
                return

            log.warning(
                'Failed attempt to send message [%(cn)d/%(tn)d] '
                'to %(chat_id)d. Will try again via '
                '%(num).2f seconds' % dict(
                    chat_id=chat_id,
                    num=WAIT_TIME,
                    tn=MAX_RETRIES,
                    cn=retries_left,
                )
            )
            time.sleep(WAIT_TIME)

        else:
            return

