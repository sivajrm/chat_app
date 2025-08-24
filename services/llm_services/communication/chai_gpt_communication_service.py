import requests
import json

from models.Agent import Agent
from services.llm_services.communication.llm_communication_service import LlmCommunicationService
from services.llm_services.providers.llm_service_provider import LLMServiceProvider
from services.llm_services.providers.llm_service_provider_factory import LLMServiceProviderFactory
from services.registry import register_service
from utils.log_config import get_logger


@register_service("chai_gpt")
class ChaiGptCommunicationService(LlmCommunicationService):

    logger = get_logger("ChaiGptCommunicationService")

    def __init__(self, llm_service_provider_factory: LLMServiceProviderFactory):
        self.headers = None
        self.provider: LLMServiceProvider = llm_service_provider_factory.get_provider("chai_gpt")
        self.prompt_format = "{safety_prompt} ###\n{prompt}"
        if self.provider is None:
            raise ValueError("Chai Gpt Communication Service is not initialized")

    def get_provider_type(self) -> str:
        return "chai_gpt"

    def send_message(self, user_agent: Agent, bot_agent: Agent, prompt, chat_history: list):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization" : "Bearer " + self.provider.auth_token
        }

        data = {
            "memory": "",
            "prompt": self.prompt_format.format(safety_prompt=bot_agent.safety_prompt, prompt=prompt),
            "bot_name": bot_agent.name,
            "user_name": user_agent.name,
            "chat_history": chat_history
        }

        attempt = 0
        while attempt < self.provider.retries:
            try:
                response = requests.post(self.provider.api_url, headers=self.headers, data=json.dumps(data))

                self.logger.debug(f"response length: {response.headers['Content-Length']}")

                if response.headers.get("Transfer-Encoding") == "chunked":
                    print("Chunked response: waiting for complete data...")

                if response.status_code in (200, 201):
                    return response
                else:
                    print(f"Request failed ({response.status_code}) reason: {response.text}, retrying...")
                    attempt += 1
            except requests.exceptions.RequestException as e:
                print(f"Error in request: {e}")
                attempt += 1

        print("All retries failed.")
        return None







