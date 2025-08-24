from collections import deque
from typing import Optional

from models.ChatHistory import ChatHistory
from models.Agent import Agent

from services.agents.agent_service_factory import AgentServiceFactory
from services.chat_service import ChatService
from services.llm_services.communication.llm_communication_service_factory import LLMCommunicationServiceFactory
from services.llm_services.providers.llm_service_provider_factory import LLMServiceProviderFactory
from utils.log_config import get_logger
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ChatDriver:

    logger = get_logger("ChatDriver")

    def __init__(self):
        self.chat_history = ChatHistory()
        self.agent_service_factory = None
        self.user_bot : Optional[Agent]  = None
        self.ai_bot : Optional[Agent] = None
        self.chat_service : Optional[ChatService] = None
        self.sentence_transformer_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1') #better with multi-qa-MiniLM-L6-cos-v1 but lags related but different topics
        self.similarity_window = deque(maxlen = 3)

    def log_agent_info(self, agent: Agent) -> None:
        self.logger.info(f"Initializing Chat agent {agent.get_colored_name()} with agent provider " + agent.llm_provider)

    def init_setup(self):
        llm_service_provider_factory = LLMServiceProviderFactory("configs/llm_provider_config.json")
        llm_communication_service_factory = LLMCommunicationServiceFactory(llm_service_provider_factory)
        self.chat_service = ChatService(llm_communication_service_factory)

        self.agent_service_factory = AgentServiceFactory("configs/agent_config.json")
        self.user_bot = self.agent_service_factory.get_agent("user_bot") #user_bot
        self.ai_bot = self.agent_service_factory.get_agent("ai_bot")

        self.log_agent_info(self.user_bot)
        self.log_agent_info(self.ai_bot)
        self.logger.info("ChatDriver initialized with necessary services")


    def did_reply_deviated_from_topic(self, message, topic_embedding):
        message_embedding = self.sentence_transformer_model.encode(message,batch_size = 32, show_progress_bar = False)

        similarity = cosine_similarity(topic_embedding.reshape(1,-1), message_embedding.reshape(1,-1))[0][0]
        self.logger.debug("Cosine similarity between topic and message is {}".format(similarity))
        self.similarity_window.append(similarity)
        return (sum(self.similarity_window) / len(self.similarity_window)) < 0.15

    def is_conversation_over(self, message: str) -> bool:
        end_keywords = ["bye", "exit", "quit", "goodbye", "see you"]
        words = set(message.lower().split())
        return not words.isdisjoint(end_keywords)

    def start_chat(self, topic: str):
        topic_embedding = self.sentence_transformer_model.encode(topic, show_progress_bar = False)
        message = f"Hello! How are you?, I would like to explore about {topic}"
        self.chat_history.get_history().clear()
        self.chat_history.add_message(self.user_bot, message)

        print(f"\033[{self.user_bot.text_color}{self.user_bot.name}: {message}\033[0m")

        while True:
            prompt = self.chat_history.history[-1]['message']
            bot_reply = self.chat_service.ask_prompt(self.user_bot, self.ai_bot, prompt, self.chat_history)


            if self.ai_bot.off_topic_check_enabled and self.did_reply_deviated_from_topic(bot_reply, topic_embedding):
                #off-topic check only for responder bot
                self.warn_other_agent(self.user_bot, topic)
                continue

            # Swap roles for next message
            prompt = self.chat_history.history[-1]['message']
            user_reply = self.chat_service.ask_prompt(self.ai_bot, self.user_bot, prompt, self.chat_history)

            ''' #do not do off-topic validation for user bots as it is a question asking bot
                if self.user_bot.off_topic_check_enabled and self.did_reply_deviated_from_topic(user_reply, topic_embedding):
                    self.warn_other_agent(self.ai_bot, topic)
                    continue
            '''

            if self.is_conversation_over(user_reply) or self.is_conversation_over(bot_reply):
                self.logger.info("Conversation over....")
                return

    def warn_other_agent(self, agent: Agent, topic):
        warning_message = "Let us not jump outside the topic " + topic
        print(f"{agent.get_colored_name()}\033[{agent.text_color}:\n{warning_message}\033[0m")
        self.chat_history.add_message(agent, warning_message)