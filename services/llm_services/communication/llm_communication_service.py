from abc import abstractmethod, ABC

from requests import Response

from models.Agent import Agent


class LlmCommunicationService(ABC):

    @abstractmethod
    def send_message(self, user_agent: Agent, bot_agent: Agent, prompt, chat_history: list) -> Response:
        raise NotImplementedError