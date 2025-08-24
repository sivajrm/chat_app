from typing import Optional

from models.ChatHistory import ChatHistory
from models.Agent import Agent
import textwrap

from services.agents.agent_service_factory import AgentServiceFactory
from services.llm_services.communication.llm_communication_service import LlmCommunicationService
from services.llm_services.communication.llm_communication_service_factory import LLMCommunicationServiceFactory
from services.llm_services.providers.llm_service_provider_factory import LLMServiceProviderFactory
from utils.response_parser import ResponseParser


class ChatDriver:
    def __init__(self):
        self.chat_history = ChatHistory()
        self.llm_service_provider_factory : Optional[LLMServiceProviderFactory] = None
        self.llm_communication_service_factory : Optional[LLMCommunicationServiceFactory] = None
        self.agent_service_factory = None
        self.user_bot : Optional[Agent]  = None
        self.ai_bot : Optional[Agent] = None

    def print_agent_info(self, agent: Agent) -> None:
        print(f"Initializing Chat agent {agent.get_colored_name()} with agent provider " + agent.llm_provider)

    def init_setup(self):
        self.llm_service_provider_factory = LLMServiceProviderFactory("configs/llm_provider_config.json")
        self.llm_communication_service_factory = LLMCommunicationServiceFactory(self.llm_service_provider_factory)
        self.agent_service_factory = AgentServiceFactory("configs/agent_config.json")
        self.user_bot = self.agent_service_factory.get_agent("siva") #user_bot
        self.ai_bot = self.agent_service_factory.get_agent("ai_bot")
        self.print_agent_info(self.user_bot)
        self.print_agent_info(self.ai_bot)

    def send_message(self, user_agent: Agent, ai_agent: Agent, prompt):
        llm_communication_service: LlmCommunicationService = self.llm_communication_service_factory.get_communication_service(ai_agent.llm_provider)
        response = llm_communication_service.send_message(user_agent, ai_agent, prompt, self.chat_history.get_history())

        if not response:
            return None

        raw_text = ResponseParser.parse(response.text)
        clean_text = ResponseParser.clean(raw_text)
        self.chat_history.add_message(ai_agent, clean_text)

        if ai_agent.llm_provider != 'terminal':
            print("\n")
            ai_agent.print_name()
            print(f"\033[{ai_agent.text_color}")
            for line in textwrap.wrap(clean_text, 60):
                print(line)
            print("\033[0m")
        return clean_text


    def start_chat(self, topic: str):
        message = f"Hello! How are you?, Do you know what's going on around {topic}"
        self.chat_history.add_message(self.user_bot, message)

        print(f"\033[{self.user_bot.text_color}{self.user_bot.name}: {message}\033[0m")

        message += "\nYou are a strict bot. Only respond with the person speaking. Do not include any narrative, actions, or descriptions"


        while True:
            prompt = self.chat_history.history[-1]['message']
            bot_reply = self.send_message(self.user_bot, self.ai_bot, prompt)
            if not bot_reply:
                print("Bot failed to respond. Ending chat.")
                break

            # Swap roles for next message
            prompt = self.chat_history.history[-1]['message']
            user_reply = self.send_message(self.ai_bot, self.user_bot, prompt)

            if not user_reply:
                print("User bot failed to respond. Ending chat.")
                break