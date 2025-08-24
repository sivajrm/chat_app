from services.llm_services.communication.chai_gpt_communication_service import ChaiGptCommunicationService
from services.llm_services.communication.terminal_communication_service import TerminalCommunicationService
from services.llm_services.providers.llm_service_provider_factory import LLMServiceProviderFactory
from services.registry import COMM_SERVICES


class LLMCommunicationServiceFactory:

    def __init__(self, llm_service_provider_factory: LLMServiceProviderFactory):
        self.communication_services = {}
        for name, cls in COMM_SERVICES.items():
            import inspect
            sig = inspect.signature(cls.__init__)
            if 'llm_service_provider_factory' in sig.parameters:
                self.communication_services[name] = cls(llm_service_provider_factory)
            else:
                self.communication_services[name] = cls()

    def get_communication_service(self, provider_id: str):
        if provider_id in self.communication_services:
            return self.communication_services[provider_id]
        else:
            raise KeyError("Communication service {} not found".format(provider_id))

