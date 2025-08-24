from models.Agent import Agent


class ChatHistory:
    def __init__(self):
        self.history = []

    def add_message(self, sender: Agent, message : str):
        self.history.append({"sender": sender.name, "message": message})

    def get_history(self) -> list:
        return self.history
