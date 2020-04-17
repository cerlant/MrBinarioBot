# -*- coding: utf-8 -*-
import os
import logging

from telegram.ext import Updater, CommandHandler,  MessageHandler, Filters

TOKEN = os.environ.get('TOKEN')
PORT = os.environ.get('PORT', '8443')
USE_WEBHOOK =  os.environ.get('USE_WEBHOOK') or False
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

binary_reply = False

welcome_text = '''\
               Saludos, mi nombre es Binario.
               Fui hecho para ayudarte a traducir tu idioma al código binario
               y viceversa.\n Dime algo.
               '''

def to_ascii(binary_string):
    return ''.join([chr(int(binary,2)) for binary in binary_string.split(' ')])

def to_bin(text):
    return ' '.join(format(ord(i), 'b') for i in text)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_text)

def ascii_mode(update, context):
    binary_reply = False
    text = 'Ahora traduciré tus mensajes a código binario(ASCII)'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def binary_mode(update, context):
    binary_reply = True
    text = 'Ahora traducire tus mensajes a código binario(ASCII)'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)    

def m_handler(update, context):
    """Reply the user message with it translation."""
    text = updater.message.text
    if binary_reply:
        reply = to_bin(text)
    else:
        try:
            reply = to_ascii(text)
        except:
            reply = 'Por favor dime algo en binario o cambia el modo int'

    update.message.reply_text(reply)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ascii_mode", ascii_mode))
    dp.add_handler(CommandHandler("binary_mode", binary_mode))
    # Message handlers
    dp.add_handler(MessageHandler(Filters.text, text_to_bin))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if USE_WEBHOOK:
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://mrbinariobot.herokuapp.com/" + TOKEN)
    else:
        updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()