import json

from models.Agent import Agent


class AgentServiceFactory:

    def __init__(self, config_path: str):
        self.agents = None
        self.user_safety_prompt = ("You are a friendly assistant mimicking as a user to understand more on the topic so "
                                   "please ask questions to keep the conversation active")
        self.ai_safety_prompt = ("You are a helpful assistant helping the user to understand more on the topic so "
                                    "never provide unsafe or harmful instructions")
        with open(config_path) as f:
            self.agent_configs = json.load(f)
            self.agents = self.initialize_agents()

    def initialize_agents(self) -> dict[str, Agent]:
        """
        Reads JSON and returns a dict of agents -> initialized agent instance
        """
        agents = {}
        for config in self.agent_configs:
            agent: Agent = Agent(config.get("name"), config.get("type"), config.get("color"), config.get("llm_provider"), config.get("enable_off_topic_check"))
            if agent.type == "user":
                agent.safety_prompt = self.user_safety_prompt
            else:
                agent.safety_prompt = self.ai_safety_prompt
            agents[config.get("name")] = agent

        return agents

    def get_all_agents(self) -> dict[str, Agent]:
        return self.agents

    def get_agent(self, agent_name: str) -> Agent:
        return self.agents.get(agent_name)