from services.llm_services.communication.chai_gpt_communication_service import ChaiGptCommunicationService
from services.llm_services.communication.terminal_communication_service import TerminalCommunicationService
from services.llm_services.providers.llm_service_provider_factory import LLMServiceProviderFactory


class LLMCommunicationServiceFactory:

    def __init__(self, llm_service_provider_factory: LLMServiceProviderFactory):
        self.communication_services = {}
        self.llm_service_provider_factory = llm_service_provider_factory
        self.communication_services['chai_gpt'] = ChaiGptCommunicationService(self.llm_service_provider_factory)
        self.communication_services['terminal'] = TerminalCommunicationService()

    def get_communication_service(self, provider_id: str):
        if provider_id in self.communication_services:
            return self.communication_services[provider_id]
        else:
            raise KeyError("Communication service {} not found".format(provider_id))

