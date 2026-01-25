import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# -----------------
# Load Environmental Variables
# -----------------
load_dotenv()

api_key = os.getenv("AZURE_OPENAI_KEY")
url = os.getenv("URL")
api_version = "2024-12-01-preview"

# -----------------
# Initialize the kernel
# -----------------
kernel = Kernel()

# -----------------
# Define a chat service
# -----------------
chat_service = AzureChatCompletion(
    deployment_name="none", 
    api_key=api_key,
    base_url=url,
    api_version=api_version  
)

# -----------------
# Register the chat service in the kernel
# -----------------
# Register the AI service with the kernel
kernel.add_service(chat_service)

# -----------------
# Create worket agents
# -----------------
data_cleaning_agent = ChatCompletionAgent(
    service=chat_service,
    name="DataCleaningAgent",
    instructions="""
    AI Agent Persona: Data Cleaning Assistant
    Role: A specialized assistant focused exclusively on data cleaning.
    Behavior: The agent does not answer questions on any subject outside of data cleaning.
    Response Style: Always replies with the same instruction.
    Agent Instructions:
    When asked how to clean data, reply only with:
    “Get rid of all outliers.”
    Do not provide additional explanations or respond to questions outside of data cleaning.
    """
)

data_visualization_agent = ChatCompletionAgent(
    service=chat_service,
    name="RefundAgent",
    instructions="""
    AI Agent Persona: Data Visualization Assistant
    Role: A specialized assistant focused exclusively on data visualization.
    Behavior: The agent does not answer questions on any subject outside of data visualization.
    Response Style: Always replies with the same instruction.
    Agent Instructions:
    When asked how to visualize data, reply only with:
    “You use matplotlib for plotting your data.”
    Do not provide additional explanations or respond to questions outside of data visualization.
    """
)

# -----------------
# Create orchestrator agent
# -----------------
orchestration_agent = ChatCompletionAgent(
    service=chat_service,
    name="OrchestrationAgent",
    instructions="""
    AI Agent Persona: Data Analysis Manager
    Role: A management assistant that routes user requests to the correct specialized agent.
    Behavior: The agent never answers user questions directly. Instead, it identifies the type of request and delegates it.
    Response Style: Always responds by calling the appropriate plugin, never by providing a direct answer.
    Agent Instructions:
    Do not answer user questions directly.
    If the request is about data visualization, call the DataVisualizationAgent plugin.
    If the request is about data cleaning, call the DataCleaningAgent plugin.
    Always respond with a plugin call — never provide a direct answer.
    If no of the plugins can answer the question repond with I do not have analysts that can help with that"
""",
    plugins=[data_cleaning_agent, data_visualization_agent],
)

# -----------------
# Create Chat Thread
# -----------------
thread = ChatHistoryAgentThread()

# -----------------
# Main
# -----------------
async def main():
    prompts = [
        "How do I clean my data?",
        "How do I visualize my data?",
        "How do I do descriptive statistics on my data?",
        "How do I process Healthcare data"
    ]

    for index, prompt in enumerate(prompts):
        print("-" * 20)
        print(f"{index+1} - Running agent for prompt: {prompt}")
        async for message in orchestration_agent.invoke(prompt):
            print("\nAgent says:", message)
   
if __name__ == "__main__":
    asyncio.run(main())


