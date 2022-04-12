import os
import random
import uuid

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from bot import detect_intent_texts


def echo(event, vk_api):
    text = detect_intent_texts(
        'quantum-ally-327819',
        str(uuid.uuid4()),
        event.text,
        language_code='ru'
    )
    
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def vk_bot(vk_token):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_bot(vk_token)


if __name__ == '__main__':
    main()
