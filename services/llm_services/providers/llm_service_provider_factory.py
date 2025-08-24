import json
import importlib

from services.llm_services.llm_service import LLMService


class LLMServiceFactory:

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config : dict = json.load(f)

    def initialize_providers(self) -> dict[str, LLMService]:
        """
        Reads JSON and returns a dict of provider_name -> initialized provider instance
        """
        providers = {}
        for key, cfg in self.config.items():
            provider_id = key
            provider_type =

            # dynamically import module
            module_name = f"services.{provider_type.lower()}"  # services.openaiprovider
            module = importlib.import_module(module_name)
            cls = getattr(module, provider_type)

            # remove "name" and "type" before passing kwargs
            kwargs = {k: v for k, v in provider_cfg.items() if k not in ("name", "type")}
            providers[provider_name] = cls(**kwargs)

        return providers