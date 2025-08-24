import json
from services.llm_services.providers.llm_service_provider import LLMServiceProvider


class LLMServiceProviderFactory:

    def __init__(self, config_path: str):
        self.providers = None
        with open(config_path) as f:
            self.config : dict = json.load(f)
            self.providers = self.initialize_providers()

    def initialize_providers(self) -> dict[str, LLMServiceProvider]:
        """
        Reads JSON and returns a dict of provider_name -> initialized provider instance
        """
        providers = {}
        for key, cfg in self.config.items():
            providers[key] = LLMServiceProvider(key, cfg.get("name"), cfg.get("api_url"), cfg.get("api_key"), cfg.get("auth_token"), cfg.get("retries"))

        return providers

    def get_provider(self, provider_id: str) -> LLMServiceProvider:
        return self.providers[provider_id]