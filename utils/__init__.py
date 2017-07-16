# -*- coding: utf-8 -*-


from .i18n import langs
from .decorators import async, Callback
from .functions import (
    send_async_message,
    send_async_location,
    edit_async_message,
    edit_async_message_markup,
)

from .botan import *
from .news import *
