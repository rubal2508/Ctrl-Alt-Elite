import openai
from django.conf import settings

from WmVoice.constants import CONTENT, MODEL_NAME, ROLE, ROLE_ASSISTANT, ROLE_SYSTEM, ROLE_USER

openai.api_key = settings.OPENAI_API_KEY


class OpenAIAgent():

    def __init__(self, agent_initialization: str, agent_name: str, read_only=False):
        self.agent_initialization = agent_initialization
        self.read_only = read_only
        self.agent_name = agent_name
        self.extras = dict()
        self.initializeFromAgentInitialization()
    

    def call(self, message):

        message = {
            ROLE: ROLE_USER,
            CONTENT: message,
        }
        self.messages.append(message)

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=self.messages,
        )
        reply = response["choices"][0]["message"]["content"]

        self.messages.append({
            ROLE: ROLE_ASSISTANT,
            CONTENT: reply,
        })

        if self.read_only:
            self.reset()

        return reply

    def initializeFromAgentInitialization(self):
        self.messages = [
            {
                ROLE: ROLE_SYSTEM,
                CONTENT: self.agent_initialization,
            },
        ]

    def reset(self):
        self.initializeFromAgentInitialization()
        self.extras = dict()
