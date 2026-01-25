import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import <TODO> # import Kernel
from semantic_kernel.connectors.ai.open_ai import <TODO> # Import AzureChatCompletion
from semantic_kernel.agents import <TODO>, <TODO> # Import ChatCompletionAgent and SequentialOrchestration
from semantic_kernel.contents import <TODO> # Import ChatMessageContent
from semantic_kernel.agents.runtime import <TODO> # Import InProcessRuntime

# -----------------
# Load environment variables
# -----------------
load_dotenv()
api_key = <TODO> # Your Azure OpenAI key
url = os.getenv("URL")
api_version = "2024-12-01-preview"

# -----------------
# Create kernel and register chat service
# -----------------
kernel = <TODO> # Initialize Kernel

# -----------------
# Define Azure Chat Completion Service
# -----------------
chat_service = <TODO>( # Initialize AzureChatCompletion
    deployment_name="none",
    api_key=<TODO>, # Your Azure OpenAI key
    base_url=url,
    api_version=api_version,
)
kernel.<TODO> # Register the chat service with the kernel

# -----------------
# Define Agents
# -----------------

creator_agent = <TODO>( # Initialize ChatCompletionAgent
    name="CreatorAgent",
    service=<TODO>, # Use the chat service defined above
    instructions=(
        f"Role: Drafts a Standard Operating Procedure (SOP) for a given industrial task."
        "Objectives:"
        "Write the SOP as a sequence of clear, numbered steps."
        "Use concise, unambiguous language suitable for industrial operations."
        "Ensure that steps follow logical order (shutdown verification → preparation → restart → post-checks)."
        "Incorporate technical details (pressures, temperatures, gauges) when relevant."
        "If supplied a REVISE label and feedback from the Critic Agent, update the SOP accordingly."
        "Workflow:"
        "Check if there is a REVISE label in the input task."
        "If REVISE is present, carefully review the Critic's feedback and update the SOP to address all points."
        "If no REVISE label, create a new SOP from scratch based on the task description."
    ),
)

critic_agent = <TODO>( # Initialize ChatCompletionAgent
    name="CriticAgent",
    service=<TODO>, # Use the chat service defined above
    <TODO>=( # Use the instructions below
        f"Role: Review the SOP against safety, compliance, and best practices."
        "Objectives:"
        "The SOP should include only a list of steps and their descriptions, no other text, tables, summaries, or other information."
        "SOP should be formatted as a numbered list. As in this example:"
        "1. Step one description."
        "2. Step two description."
        "3. Step three description."
        "..."
        "Only provide feedback on:"
        "- steps being numbered and described"
        "- each step must include: Action, Responsible Party, Safety Considerations, Tools/Equipment Needed"
        "Workflow:"
        "If the SOP is satisfactory, respond with 'APPROVED' and show the final SOP."
        "Otherwise, provide detailed feedback for revisions and add label 'REVISE'."
        "include the original SOP text in your response for context, labeled as 'Original SOP:'"
    ),
)

# -----------------
# Define Sequential Orchestration (single critic pass)
# -----------------

def agent_response_callback(message: <TODO>) -> None: # include the arugent chat message content
    print(f"\n Agent Responsed: {message.name}\n")

sequential_orchestration = SequentialOrchestration(
    members=[<TODO>, <TODO>], # Use the agents defined above
    agent_response_callback=a<TODO> # Use the agent_response_callback defined above
)

initial_task = """
Restarting a Gas Turbine after a Shutdown for Maintenance
"""

# -----------------
# Run orchestration
# -----------------
async def main():
    runtime = <TODO> # Initialize InProcessRuntime
    <TODO> # Start the runtime

    approved = False
    iteration = 1
    current_task = <TODO> # Use the initial_task defined above

    while not approved and iteration < 10:
        print(f"\n=== Iteration {iteration} ===\n")
        print("-------------------------------------")
        print(f"\n--- Current Task ---\n{current_task}\n")
        print("-------------------------------------")

        orchestration_result = await <TODO>( # Invoke the orchestration
            task=<TODO>, # Use the current task defined above
            runtime=<TODO>, # Use the runtime defined above
        )

        final_report = await orchestration_result.<TODO>() # Get the final report
        print("-------------------------------------")
        print(f"\n--- Final Report ---\n{final_report}\n")
        print("-------------------------------------")

        current_task = final_report

        if "APPROVED" in final_report.<TODO>: # Check if the final report contains "APPROVED", make it robust to case sensitivity
            approved = True
            print("\n=== SOP Approved ===\n")
        else:
            print("\n=== SOP Requires Revision ===\n")
            iteration += 1

    await runtime.stop_when_<TODO>() # Stop the runtime when idle



if __name__ == "__main__":
    print("\n=== Starting Document Creator-Critic Orchestrator ===\n")
    asyncio.run(<TODO>) # Run the main function asynchronously