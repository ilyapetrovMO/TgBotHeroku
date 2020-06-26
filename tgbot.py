import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import http.client
import json
import http.client
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1231896443:AAF9pBdS3iXQhz_7gZwtOFPIC6S3Dto35ek'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Введите Id контракта (пр. /getBalance 1)')

def getBalance(update, context):
    try:
        logger("DEBUG:" + update.message.text[12:])
        int(update.message.text[12:])
    except ValueError:
        update.message.reply_text('Введите число')
        return

    clnt = http.client.HTTPConnection('test-ua.herokuapp.com', timeout=10)
    clnt.request('GET','/api/Report?contractId=' + update.message.text[12:])
    res = clnt.getresponse()
    resBody = res.read().decode('utf-8')
    clnt.close()
    resThing = json.loads(resBody)

    update.message.reply_text(resThing['balance'])

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введите Id контракта(пр. 1)')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getBalance", getBalance))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://tgbotheroku.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()