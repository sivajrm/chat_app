
class Agent:
    def __init__(self, name, text_color, llm_provider, enable_off_topic_check = False):
        self.name = name
        self.text_color = text_color
        self.llm_provider: str = llm_provider
        self.off_topic_check_enabled = enable_off_topic_check

    def print_name(self):
        print(f"{self.get_colored_name()}:\033[0m")

    def get_colored_name(self):
        return f"\033[{self.text_color}{self.name}\033[0m"