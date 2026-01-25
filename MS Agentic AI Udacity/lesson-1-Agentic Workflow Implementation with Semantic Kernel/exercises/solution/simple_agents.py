import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import KernelArguments

# -----------------
# Load environment
# -----------------
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
BASE_URL = os.getenv("URL")
API_VERSION = "2024-12-01-preview"
DEPLOYMENT = "gpt-4.1-mini"

# -----------------
# Kernel & service
# -----------------
kernel = Kernel()
chat_service = AzureChatCompletion(
    deployment_name=DEPLOYMENT,
    api_key=AZURE_OPENAI_KEY,
    base_url=f"{BASE_URL}{DEPLOYMENT}",
    api_version=API_VERSION
)
kernel.add_service(chat_service)

# -----------------
# Helper to create agents
# -----------------
def create_agent(name: str, instructions: str, temperature=0.7, max_tokens=300):
    settings = OpenAIChatPromptExecutionSettings()
    settings.temperature = temperature
    settings.max_tokens = max_tokens
    return ChatCompletionAgent(
        service=chat_service,
        name=name,
        instructions=instructions,
        arguments=KernelArguments(settings)
    )

# -----------------
# Define agents
# -----------------
data_analyst_agent = create_agent(
    "DataAnalyst",
    """
You are an expert in data analysis and statistics.
If the question is about data analysis, statistics, or probability, answer it in detail.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

math_agent = create_agent(
    "MathAgent",
    """
You are a mathematician.
If the question is about mathematics (arithmetic, algebra, geometry, number theory), answer it.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

translator_agent = create_agent(
    "TranslatorAgent",
    """
You are a translator.
If the request is to translate text between languages, do so.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

literature_agent = create_agent(
    "LiteratureAgent",
    """
You are a literature expert.
If the question is about literature, books, or literary analysis, answer it.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

agents = [data_analyst_agent, math_agent, translator_agent, literature_agent]

# -----------------
# Main
# -----------------
async def main():
    prompts = [
        "What is the average of 11,22,33",
        "Summarize the plot of Romeo and Juliet",
        "List the first 5 prime numbers",
        "Translate 'Good morning' into Spanish",
        "Give me a statistical summary for this data: 233,555,9866,2345,77",
        "Who won the World Cup in 2010?"
    ]

    for i, prompt in enumerate(prompts, start=1):
        print("\n" + "-" * 20)
        print(f"Prompt {i}: {prompt}")
        for agent in agents:
            print(f"\n[{agent.name}]")
            async for message in agent.invoke(prompt):
                print(f"{message}\n", end="")

if __name__ == "__main__":
    asyncio.run(main())
