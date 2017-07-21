# -*- coding: utf-8 -*-

import weakref
import telegram
from cache import Context
import settings
from utils import (
    langs,
    send_async_message,
    edit_async_message,
    get_random_news,
    get_hot_news,
    get_rare,
)

from functools import wraps
import logging
log = logging.getLogger(__name__)
import pickle



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
        if value in (_('BACK_BUTTON'), _('CANCEL_BUTTON')):
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
                telegram.KeyboardButton(_('MEGAFON_STATE_TEXT')),
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
            log.info(type(value))
            log.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            self.new_state(KremlinMenuState)
        elif value == _('MEGAFON_STATE_TEXT'):
            self.new_state(MegafonMenuState)
        elif value == '/start':
            self.on_enter('qazxswedc')


class BaseOptionMenuState(BaseState):

    parent = MainMenuState

    def on_enter(self, text=None):
        if text is None:
            text = '1234567890'

        markup = telegram.ReplyKeyboardMarkup(
            [[
                telegram.KeyboardButton(_('NEW_BUTTON')),
                telegram.KeyboardButton(_('MAIN_BUTTON')),
                telegram.KeyboardButton(_('CUBES_BUTTON')),
            ], [telegram.KeyboardButton(_('BACK_BUTTON')),
            ]],
            resize_keyboard=True,
        )
        send_async_message(
            self.bot,
            self.update,
            text,
            markup=markup,
        )

    def on_input(self, value):
        if value == _('BACK_BUTTON'):
            self.new_state(MainMenuState)
        else:
            value_mapping = {
                _('NEW_BUTTON'): 0,
                _('MAIN_BUTTON'): 1,
                _('CUBES_BUTTON'): 2,
            }
            v = value_mapping.get(value)
            return v


class KremlinMenuState(BaseOptionMenuState):
    @back_button
    def on_input(self, value):
        button = super(KremlinMenuState, self).on_input(value)
        category = u'Kremlin'
        send_news(self.bot, self.update, category, button, initial=True)


class MegafonMenuState(BaseOptionMenuState):
    @back_button
    def on_input(self, value):
        button = super(MegafonMenuState, self).on_input(value)
        category = u'Megafon'
        if button == 0:
            text = get_random_news(category)
        elif button == 1:
            text = get_hot_news(category)
        elif button == 2:
            text = get_rare(chat_id=self.update.message.chat_id, category=category)
        else:
            text = '12345'
        send_async_message(self.bot, self.update, text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=1)


def send_news(bot, update, category, button, detailed=False, initial=False):
    if button == 0:
        text = get_random_news(category)
    elif button == 1:
        text = get_hot_news(category)
    elif button == 2:
        text = get_rare(chat_id=update.message.chat_id, category=category)

    if detailed is False:
        txt = _('MORE_BUTTON')
    else:
        txt = _('LESS_BUTTON')

    func = encode_callback(send_news)
    cb = pickle.dumps((func, (category, button, (not detailed),)))
    keyboard = [[
        telegram.InlineKeyboardButton(txt, callback_data=cb),
    ]]
    markup = telegram.InlineKeyboardMarkup(keyboard)

    if initial is True:
        f = send_async_message

    else:
        f = edit_async_message
    f(
        bot,
        update,
        text,
        parse_mode=telegram.ParseMode.MARKDOWN,
        markup=markup
    )


   # send_async_message(bot, update, text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=1)



def callback_query_handler(bot, update):
    query = update.callback_query
    try:
        func_id, args = pickle.loads(query.data.encode('utf-8'))
        #func_id, args = pickle.loads(query.data.encode('utf-8'))
    except Exception as err:
        log.exception(err)
    else:
        func = decode_callback(func_id)
        log.info(
            (
                u'chat:{chat} user:{u.name} id:{u.id} '
                u'callback request: {fn.func_name}'
            ).format(
                u=query.from_user,
                chat=query.message.chat_id,
                fn=func,
            )
        )
        if callable(func):
            func(bot, update, args[0], args[1], detailed=args[2])

callback_functions = [
    send_news,
]


def encode_callback(func):
    return callback_functions.index(func)


def decode_callback(index):
    if index < len(callback_functions):
        return callback_functions[index]





