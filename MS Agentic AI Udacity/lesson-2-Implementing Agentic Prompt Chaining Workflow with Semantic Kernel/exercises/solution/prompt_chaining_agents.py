import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import KernelArguments
from semantic_kernel.functions import kernel_function

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
# Weather plugin
# -----------------
class WeatherPlugin:
    @kernel_function(description="Get weather forecast for a given location")
    async def search(self, location: str) -> str:
        # Simulated weather data; replace with real API call if desired
        return (
            f"Weather forecast for {location}: High 95°F, Low 78°F, "
            "Humidity 80%, Thunderstorms expected in the afternoon."
        )

kernel.add_plugin(plugin=WeatherPlugin(), plugin_name="Weather")

# -----------------
# Helper to create agents
# -----------------
def create_agent(name: str, instructions: str, temperature=0.7, max_tokens=600):
    settings = OpenAIChatPromptExecutionSettings()
    settings.temperature = temperature
    settings.max_tokens = max_tokens
    return ChatCompletionAgent(
        kernel=kernel,  
        service=chat_service,
        name=name,
        instructions=instructions,
        arguments=KernelArguments(settings)
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

agents = [safety_agent, regulation_agent, weather_agent, final_agent]

# -----------------
# Main chaining logic
# -----------------
async def main():
    location = "Houston, Texas"
    current_output = f"Prepare the safety plan for a hydrocarbon processing plant in {location} taking into consideration the current weather forecast"

    for agent in agents:
        print("\n" + "-" * 20)
        print(f"\n--- {agent.name} ---")
        async for message in agent.invoke(current_output):
            current_output = str(message)
            print(current_output)

    print("\n" + "-" * 20)
    print("\n=== FINAL SERVICE PLAN ===")
    print(current_output)

if __name__ == "__main__":
    asyncio.run(main())
