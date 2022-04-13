import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from logger import TelegramLogsHandler

logger = logging.getLogger(__name__)


def error(update, context):
    logger.exception('У бота Telegram проблема')


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def send_message(update, context):
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    text = detect_intent_texts(
        project_id,
        update.effective_chat.id,
        update.message.text,
        language_code='ru'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    tg_log_token = os.getenv('TG_LOG_TOKEN')
    chat_id = os.getenv('TG_LOG_CHAT_ID')

    log_bot = telegram.Bot(token=tg_log_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    logger.info('Бот Telegram запущен')
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
