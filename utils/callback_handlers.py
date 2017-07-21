# -*- coding: utf-8 -*-


def button(bot, update):
    if update.callback_query.data == 'More':
        headers = get_other_hot_news()
        edit_async_message_markup(bot, update, message_id=update.callback_query.message.message_id, reply_markup='')
        #bot.editMessageReplyMarkup(chat_id=update.callback_query.message.chat.id, message_id=update.callback_query.message.message_id, reply_markup='')
        send_async_message(bot, update, headers, markup=keyboard, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=1)
        #bot.sendMessage(chat_id=update.callback_query.message.chat.id, text=headers, reply_markup=keyboard, parse_mode='html', disable_web_page_preview=1)
    else:
        bot.editMessageReplyMarkup(chat_id=update.callback_query.message.chat.id, message_id=update.callback_query.message.message_id, reply_markup='')
