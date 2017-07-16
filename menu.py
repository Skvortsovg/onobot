# -*- coding: utf-8 -*-

import weakref
import telegram
from cache import Context
import settings
from utils import (
    async,
    langs,
    send_async_message,
)

from functools import wraps
import logging
log = logging.getLogger(__name__)


class BaseState(object):
    """ Initial session state """

    # Parent class for "back" and "cancel" buttons
    parent = None

    def __init__(self, bot, update):

        self.bot = weakref.proxy(bot)
        self.update = weakref.proxy(update)
        self.ctx = Context(update.message.chat_id)

        ctx = self.ctx
        ctx.p_get_state()
        ctx.p_get_lang()
        ctx.p_get_authorized()
        state, lang, is_authodized, = ctx.apply()

        log.info(
            (
                u'chat:{chat} user:{u.name} id:{u.id} '
                u'state is {state}.'
            ).format(
                u=update.message.from_user,
                chat=update.message.chat_id,
                state=str(state)
                #state=str(state).encode('utf-8'),
            )
        )

        if lang is None:
            lang = settings.DEFAULT_LANGUAGE
            ctx.p_set_lang(lang)
            ctx.apply()

        langs[lang].install()

        if not state:
            log.info(
                (
                    u'chat:{chat} user:{u.name} id:{u.id} '
                    u'state is {state}. Going to MainMenuState'
                ).format(
                    u=update.message.from_user,
                    chat=update.message.chat_id,
                    state=state,
                )
            )
            self.new_state(MainMenuState)
        else:
            klass = globals().get(state, MainMenuState.__name__)

            self.__class__ = klass
            #value = update.message.text.encode('utf-8').strip()
            value = update.message.text.strip()
            self.on_input(value)

    def on_enter(self, **kwargs):
        """ This method is called when ctx enters new state """

    def on_input(self, value):
        """ This method is called on ctx input """

    def __str__(self):
        return type(self).__name__

    def save_state(self, timeout=None):
        """ Save current ctx to storage """
        name = str(self)

        log.info(
            (
                u'chat:{chat} user:{u.name} id:{u.id} '
                u'saving session state:{name} timeout:{tmout}'
            ).format(
                u=self.update.message.from_user,
                chat=self.update.message.chat_id,
                name=name,
                tmout=timeout,
            )
        )

        self.ctx.p_set_state(str(self), timeout=timeout)
        self.ctx.apply()

    def new_state(self, state, **kwargs):
        """ Enter another state """

        parent = str(self)

        log.info(
            (
                u'chat:{chat} user:{u.name} id:{u.id} '
                u'enter new state:{state} from:{parent}'
            ).format(
                u=self.update.message.from_user,
                chat=self.update.message.chat_id,
                state=state,
                parent=parent,
            )
        )

        if state is not None:
            log.info('state is {st_type} = {state}'.format(st_type=type(state), state=state))
            self.__class__ = state
            # self.parent = parent
            self.save_state(timeout=settings.SESSION_TIMEOUT)
            self.on_enter(**kwargs)
        else:
            warn_msg = (
                u'chat:{chat} user:{u.name} id:{u.id} '
                u'WARNING! State can not be "None" (probably logic error). '
                u'Doing nothing'
            ).format(
                u=self.update.message.from_user,
                chat=self.update.message.chat_id,
            )
            log.warning(warn_msg)


def back_button(func):
    @wraps(func)
    def wrapper(self, value):
        if value in (_('LABEL_BACK_BUTTON'), _('LABEL_CANCEL_BUTTON')):
            log.info(
                (
                    u'chat:{chat} user:{u.name} id:{u.id} '
                    u'user clicked "back" or "cancel" button'
                ).format(
                    u=self.update.message.from_user,
                    chat=self.update.message.chat_id,
                )
            )

            self.new_state(self.parent)
        else:
            return func(self, value)
    return wrapper


class MainMenuState(BaseState):

    def on_enter(self, text=None, **kwargs):
        if text is None:
            text=_('MAIN_MENU_STATE_TEXT')

        markup = telegram.ReplyKeyboardMarkup(
            [[
                telegram.KeyboardButton(_('KREMLIN_STATE_TEXT')),
            ], [
                telegram.KeyboardButton(_('KREMLIN_STATE_TEXT')),
            ]],
            resize_keyboard=True,
        )

        send_async_message(self.bot, self.update, text, markup=markup, **kwargs)

    def on_input(self, value):

        log.info(
           (
               u'chat:{chat} user:{u.name} id:{u.id} '
               u'value is {value}.'
           ).format(
               u=self.update.message.from_user,
               chat=self.update.message.chat_id,
               value=value,
           )
        )
        if value == _('KREMLIN_STATE_TEXT'):
            self.on_enter('MEGAFON')
        elif value == _('KREMLIN_STATE_TEXT'):
            self.on_enter('KREMLIN')
        elif value == '/start':
            self.on_enter('terewrwerwerwerw')


