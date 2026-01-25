import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import <TODO> # import kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import <TODO> # import Kernel Arguments
from semantic_kernel.functions import <TODO> # import kernel function

# -----------------
# Load environment
# -----------------
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
BASE_URL = os.getenv("URL")
API_VERSION = "2024-12-01-preview"
DEPLOYMENT = <TODO> # use the gpt-4.1-mini deployment

# -----------------
# Kernel & service
# -----------------
kernel = Kernel()
chat_service = <TODO>( # use the correct chat completion class
    deployment_name=DEPLOYMENT,
    api_key=AZURE_OPENAI_KEY,
    base_url=f"{BASE_URL}{DEPLOYMENT}",
    api_version=API_VERSION
)
kernel.add_service(<TODO>) # add the correct chat service object

# -----------------
# Weather plugin
# -----------------
class WeatherPlugin:
    @<TODO>(description="Get weather forecast for a given location") # use the kernel function decorator
    async def search(self, location: str) -> <TODO>: # use the correct annotation type for what is returned by the function
        # Simulated weather data; replace with real API call if desired
        return (
            f"Weather forecast for {location}: High 95°F, Low 78°F, "
            "Humidity 80%, Thunderstorms expected in the afternoon."
        )

kernel.<TODO>(plugin=WeatherPlugin(), plugin_name="Weather") # use the appropriate method call for plugins

# -----------------
# Helper to create agents
# -----------------
def create_agent(name: str, instructions: str, temperature=0.7, max_tokens=600):
    settings = <TODO>() # use the appropriate chat settings class
    settings.temperature = temperature
    settings.max_tokens = max_tokens
    return ChatCompletionAgent(
        kernel=<TODO>,  # Pass the kernel
        service=<TODO>, # Pass the chat service
        name=name,
        instructions=instructions,
        arguments=<TODO>(<TODO>) # Use the correct arguments class with the settings argument
    )

# -----------------
# Agents
# -----------------
safety_agent = create_agent(
    "SafetyAgent",
    "You are a safety engineer specializing in hydrocarbon processing plants. "
    "Create a detailed SAFETY PLAN.",
    temperature=0.3  # Low temp → high determinism. Safety plans must be precise, repeatable, and standards-aligned.
                     # 0.3 is ideal to minimize creative drift and ensure factual consistency.
)
regulation_agent = create_agent(
    "RegulationAgent",
    "You are an expert in industrial regulations. "
    "Integrate OSHA, EPA, and API/NFPA standards into the SAFETY PLAN.",
    temperature=0.35  # Slightly higher than SafetyAgent to allow merging of multiple regulatory frameworks,
                      # but still low enough to avoid hallucinations. Originally 0.4; reduced to 0.35 for stricter compliance.
)
weather_agent = create_agent(
    "WeatherAgent",
    "Adapt the plan for forecasted weather conditions."
    "Use your knowledge to add procedures and steps that take into account the expected weather",
    temperature=0.55  # Mid-range temp → allows contextual creativity for scenario planning.
                      # Raised from 0.5 to 0.55 to encourage richer adaptation without losing structure.
)
final_agent = create_agent(
    "FinalIntegrationAgent",
    "You are a senior plant manager. Integrate all sections into a coherent SERVICE PLAN.",
    temperature=0.7  # Higher temp → better narrative flow and integration of diverse inputs.
)

agents = <TODO> # Add all agents to a list

# -----------------
# Main chaining logic
# -----------------
async def main():
    location = "Houston, Texas"
    current_output = f"Prepare the safety plan for a hydrocarbon processing plant in {location} taking into consideration the current weather forecast"

    for <TODO> # call all agents in sequence passing prompts
        print("\n" + "-" * 20)
        print(f"\n--- {agent.name} ---")
        async for message in agent.invoke(current_output):
            current_output = <TODO> # Update the output for the next prompt
            print(current_output)

    print("\n" + "-" * 20)
    print("\n=== FINAL SERVICE PLAN ===")
    print(<TODO>) # Print final plan

if __name__ == "__main__":
    asyncio.run(main())
