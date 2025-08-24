import requests

from models.Agent import Agent
from services.llm_services.communication.llm_communication_service import LlmCommunicationService
from services.registry import register_service


@register_service("terminal")
class TerminalCommunicationService(LlmCommunicationService):

    def get_provider_type(self) -> str:
        return "terminal"

    def send_message(self, user_agent: Agent, bot_agent: Agent, prompt, chat_history: list):
        bot_agent.print_name()
        prompt_response = input()
        response = requests.Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        response._content = str('{"model_output" : "' + prompt_response + '"}').encode('utf-8')
        response.headers['Content-Length'] = str(len(response._content))
        return response
