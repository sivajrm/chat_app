import json

from models.Agent import Agent


class AgentServiceFactory:

    def __init__(self, config_path: str):
        self.agents = None
        with open(config_path) as f:
            self.agent_configs = json.load(f)
            self.agents = self.initialize_agents()

    def initialize_agents(self) -> dict[str, Agent]:
        """
        Reads JSON and returns a dict of agents -> initialized agent instance
        """
        agents = {}
        for config in self.agent_configs:
            agents[config.get("name")] = Agent(config.get("name"), config.get("color"), config.get("llm_provider"))

        return agents

    def get_agent(self, agent_name: str) -> Agent:
        return self.agents[agent_name]