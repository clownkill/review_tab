import logging

import os
import random
import uuid

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_detect_texts import detect_intent_texts
from logger import TelegramLogsHandler


logger = logging.getLogger(__name__)


def send_message(project_id, event, vk_api):
    text = detect_intent_texts(
        project_id,
        str(uuid.uuid4()),
        event.text,
        language_code='ru'
    )
    if not text:
        return
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def vk_bot(project_id, vk_token, logger):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                send_message(project_id, event, vk_api)
            except Exception as err:
                logger.error('Бот VK упал с ошибкой:')
                logger.error(err, exc_info=True)


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    tg_log_token = os.getenv('TG_LOG_TOKEN')
    chat_id = os.getenv('TG_LOG_CHAT_ID')
    project_id = os.getenv('GOOGLE_PROJECT_ID')

    log_bot = telegram.Bot(token=tg_log_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    logger.info('Бот VK запущен')
    vk_bot(project_id, vk_token, logger)


if __name__ == '__main__':
    main()
