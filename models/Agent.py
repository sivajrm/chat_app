
class Agent:
    def __init__(self, name, text_color, llm_provider):
        self.name = name
        self.text_color = text_color
        self.llm_provider: str = llm_provider
