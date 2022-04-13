import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def load_training_phrases(training_file):
    with open(training_file) as json_file:
        training_phrases = json.load(json_file)
    return training_phrases


def main():
    load_dotenv()
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    training_data = load_training_phrases('phrases.json')

    for display_name, training_intent in training_data.items():
        training_phrases_parts = training_intent['questions']
        message_texts = [training_intent['answer']]

        create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
