import os
import random
import uuid

import vk_api as vk
from google.cloud import dialogflow
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


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


def echo(event, vk_api):
    text = detect_intent_texts(
        'quantum-ally-327819',
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
