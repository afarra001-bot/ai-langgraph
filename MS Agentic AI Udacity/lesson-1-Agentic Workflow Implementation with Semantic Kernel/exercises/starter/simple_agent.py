import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import <TODO> # import kernel
from semantic_kernel.connectors.ai.open_ai import <TODO>, <TODO> # import Azure Chat and Execution Settings
from semantic_kernel.agents import <TODO>  # import Chat Completion Agent
from semantic_kernel.functions import <TODO> # import Kernel Arguments

# -----------------
# Load environment
# -----------------
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
BASE_URL = os.getenv("URL")
API_VERSION = "2024-12-01-preview"
DEPLOYMENT = <TODO> # define the correct LLM deployment

# -----------------
# Kernel & service
# -----------------
kernel = <TODO> # initialize the kernel
chat_service = <TODO>( # define the correct chat service object
    deployment_name=DEPLOYMENT,
    api_key=AZURE_OPENAI_KEY,
    base_url=f"{BASE_URL}{DEPLOYMENT}",
    api_version=API_VERSION
)
kernel.add_service(<TODO>) # add the chat service to the kernel

# -----------------
# Helper to create agents
# -----------------
def create_agent(name: str, instructions: str, temperature=0.7, max_tokens=300):
    settings = <TODO> # instantiate the execution settings object
    settings.<TODO> = temperature # assign temperature to the correct settings object argument
    settings.<TODO> = max_tokens # assign max tokens to the correct settings object argument
    return ChatCompletionAgent(
        service=chat_service,
        name=name,
        instructions=instructions,
        arguments=<TODO>(<TODO>) # instantiate the arguments objects with the settings object as argument
    )

# -----------------
# Define agents
# -----------------
data_analyst_agent = <TODO>( # use the correct helper function
    "DataAnalyst",
    """
You are an expert in data analysis and statistics.
If the question is about data analysis, statistics, or probability, answer it in detail.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

math_agent = <TODO>( # use the correct helper function
    "MathAgent",
    """
You are a mathematician.
If the question is about mathematics (arithmetic, algebra, geometry, number theory), answer it.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

translator_agent = <TODO>( # use the correct helper function
    "TranslatorAgent",
    """
You are a translator.
If the request is to translate text between languages, do so.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

literature_agent = <TODO>( # use the correct helper function
    "LiteratureAgent",
    """
You are a literature expert.
If the question is about literature, books, or literary analysis, answer it.
If it is not, respond with: "I cannot answer this question as it is outside my expertise."
"""
)

agents = <TODO> # add all agents to a list

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
        for agent in <TODO>: # iterate through the agents list
            print(f"\n[{agent.name}]")
            async for message in agent.<TODO>(prompt): # call the agent object's invoke method
                print(f"{<TODO>}\n", end="") # print the agents response message

if __name__ == "__main__":
    asyncio.run(main())
