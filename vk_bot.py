import os

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


def vk_bot(vk_token):
    vk_session = vk_api.VkApi(token=vk_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print(f'Для меня от: {event.user_id}')
            else:
                print(f'От меня для: {event.user_id}')
            print(f'Текст: {event.text}')


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_bot(vk_token)


if __name__ == '__main__':
    main()
