**Steps:**
1. Agent Configuration:
    The agents (user agent(Terminal or AI based) and AI agent) are configured via agent_config.json. Each agent can select its LLM service provider

2. LLM Service Provider configuration:
   LLM service provider related configs are maintained through the llm_provider_config.json. Each service provider can maintain their api-url, api-key, auth-token(can be extended to retrive from an oauth server), number of retries if there is a service error.

3. Chat Driver:
   The ChatDriver class acts as the main driver of the application. It initializes the necessary service classes, agents(user/ai based) and manages the flow of the interaction(conversation exchange, off-topic detection, end conversation detection).

4. Off-Topic Check:
   Implemented a feature to monitor the AI bot’s responses using Sentence transformer model and cosine simularity. If the responder ai bot goes off-topic, the chat app automatically interrupts and sends a message to guide the bot back to the relevant topic on
   behalf of the user. Configured the threshold as below 15% to detect as bot is going off-topic.

**Extensibility:
**
LLM Services:
The LLM services used by the agents are modular and extensible. You can plug in any service provider (e.g., OpenAI, HuggingFace), provided the implementation is integrated in the code.

Terminal Communication:
When the user interacts with the AI bot, there is a support to interact for the end-user using TerminalCommunicationService class, which provides end user input as prompts to the AI agent to carry the conversation.

Things to improve:
1. Communication classes can be extended to use a common Request exchance class
2. Support for web-sockets as this is a chat-app so using a web-socket will improve the latency and consumption of network resources
3. Extend this to a multi-agent chat room concept
