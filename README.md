# Chat App

## Overview

This application allows a user and AI agent to interact in a configurable chat environment. It can also accept Agent-Agent chat on a topic agreed in the beginning. The system is modular and supports multiple LLM service providers, off-topic detection, and terminal-based communication.

---

## Steps

### 1. Agent Configuration

The agents (user agent — Terminal or AI based — and AI agent) are configured via `agent_config.json` containing name, type(acting as user/ai bot), color, llm_provider(terminal /chai_gpt). 
Each agent(user / ai bots) can select from the config json during runtime its preferred agent config to use.

### 2. LLM Service Provider Configuration

The LLM service provider configurations are maintained in `llm_provider_config.json`. Each provider can define:

* API URL
* API key / auth token (can be extended to retrieve from an OAuth server)
* Number of retries for service errors

This allows flexible integration of different providers.

### 3. Chat Driver

The `ChatDriver` class acts as the main driver of the application. Responsibilities include:

* Initializing necessary service classes and agents. Choose the user-bot and ai-bot to use for this interaction
* Managing conversation flow
* Detecting off-topic responses
* Detecting end-of-conversation events (bye or exit or quit or goodbye or see you)

### 4. Off-Topic Check

A feature to monitor the AI bot’s responses using a **Sentence Transformer model** and **cosine similarity**.

* If the AI responder goes off-topic, the chat app automatically interrupts and sends a message on behalf of the user to maintain topic relevance.
* A similarity threshold of **15%** is used to flag off-topic responses.

### 5. Extensibility: LLM Services

The LLM services used by agents are **modular and extensible**. You can integrate any service provider (e.g., OpenAI, HuggingFace) as long as the implementation is provided in the code.

### 6. Terminal Communication

For user interaction, the `TerminalCommunicationService` class allows the end-user to provide prompts directly to the AI agent via the terminal.

---

## Things to Improve

* Refactor communication classes to use a common **Request Exchange** class
* Add **web-socket support** for lower latency and better network efficiency
* Extend the system to a **multi-agent chat room** concept

---

## Sample Output

C:\Users\Siva\PyCharmMiscProject\.venv\Scripts\python.exe F:\PersonalProjects\chat_app\app.py 
2025-09-06 21:34:56,590 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-09-06 21:34:56,590 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: multi-qa-MiniLM-L6-cos-v1
2025-09-06 21:34:59,686 - ChatDriver - INFO - ChatDriver initialized with necessary services
Welcome to Chat App.... 
Loading pre-defined available bots for use...

Type: user
Name                 LLM Provider        
----------------------------------------
siva        terminal            
user_bot    chai_gpt            

Type: ai
Name                 LLM Provider        
----------------------------------------
ai_bot      chai_gpt            
Please enter your user bot name to use: siva
Please enter your ai bot name to use: ai_bot
2025-09-06 21:35:14,637 - ChatDriver - INFO - Initializing Chat agent siva as User bot with agent provider terminal
2025-09-06 21:35:14,637 - ChatDriver - INFO - Initializing Chat agent ai_bot as AI bot with agent provider chai_gpt
Bot acting as user would like to explore about : Cricket game
siva: Hello! How are you?, I would like to explore about Cricket game


ai_bot:
"I'm great, thanks! Nice to meet you...?"

siva:
Let us not jump outside the topic Cricket game


ai_bot:
"Okay, I love cricket! Tell me, what's your favorite format
- Tests, ODIs or T20s?"

siva:
How many players play the game??


ai_bot:
"In cricket, there are two teams, each consisting of 11
players. So, a total of 22 players participate in a match.
One team bats while the other bowls and fields. The game is
played on a large oval-shaped field with a rectangular pitch
in the center."

siva:
Bye

2025-09-06 21:35:55,498 - ChatDriver - INFO - Conversation over....


Welcome to Chat App.... 
Loading pre-defined available bots for use...

Type: user
Name                 LLM Provider        
----------------------------------------
siva        terminal            
user_bot    chai_gpt            

Type: ai
Name                 LLM Provider        
----------------------------------------
ai_bot      chai_gpt            
Please enter your user bot name to use: 
