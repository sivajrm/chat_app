import textwrap

from models.Agent import Agent
from models.ChatHistory import ChatHistory
from services.llm_services.communication.llm_communication_service_factory import LLMCommunicationServiceFactory
from utils.log_config import get_logger
from utils.response_parser import ResponseParser
from services.llm_services.communication.llm_communication_service import LlmCommunicationService


class ChatService:

    def __init__(self, llm_communication_service_factory : LLMCommunicationServiceFactory):
        self.llm_communication_service_factory = llm_communication_service_factory
        self.logger = get_logger("ChatService")

    def ask_prompt(self, user_agent: Agent, ai_agent: Agent, prompt, chat_history: ChatHistory) -> str | None:
        llm_communication_service: LlmCommunicationService = self.llm_communication_service_factory.get_communication_service(ai_agent.llm_provider)
        response = llm_communication_service.send_message(user_agent, ai_agent, prompt, chat_history.get_history())
        self.logger.debug("Response received for {} from {} provider".format(ai_agent.name, llm_communication_service))

        if not response:
            print(f"Bot '{ai_agent.get_colored_name()}' failed to respond. Ending chat.")
            return None

        raw_text = ResponseParser.parse(response.text)
        clean_text = ResponseParser.clean(raw_text)
        chat_history.add_message(ai_agent, clean_text)

        if ai_agent.llm_provider != 'terminal':
            print("\n")
            ai_agent.print_name()
            for line in textwrap.wrap(clean_text, 60):
                print(f"\033[{ai_agent.text_color}{line}")
            print("\033[0m")
        return clean_text