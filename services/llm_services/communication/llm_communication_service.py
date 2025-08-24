
from models.Agent import Agent


class LLMService:

    def send_message(self, user_agent: Agent, bot_agent: Agent, prompt, chat_history:dict):
        raise NotImplementedError