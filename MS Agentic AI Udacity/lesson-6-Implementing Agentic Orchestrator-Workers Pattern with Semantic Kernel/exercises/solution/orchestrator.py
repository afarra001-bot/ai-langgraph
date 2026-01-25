import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel.agents import (
    ChatCompletionAgent,
    StandardMagenticManager,
    MagenticOrchestration,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.agents.runtime import InProcessRuntime

# -----------------
# Load environment variables
# -----------------
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_KEY")
url = os.getenv("URL")
api_version = "2024-12-01-preview"

# -----------------
# Target industry 
# -----------------
target_industry = "avaiation"

# -----------------
# Define Azure Chat Completion Service
# -----------------
chat_service = AzureChatCompletion(
    deployment_name="none",
    api_key=api_key,
    base_url=url,
    api_version=api_version,
)

# -----------------
# Agents Definitions
# -----------------
orchestrator = ChatCompletionAgent(
    name="Orchestrator",
    description="Plans, delegates, and synthesizes a market analysis report.",
    instructions="",  # injected dynamically later
    service=chat_service,
)

news_agent = ChatCompletionAgent(
    name="NewsAgent",
    description="Gathers and summarizes recent market news.",
    instructions="You are a news analyst. Execute only the instruction given.",
    service=chat_service,
)

competitor_agent = ChatCompletionAgent(
    name="CompetitorAgent",
    description="Analyzes competitors’ strategies and performance.",
    instructions="You are a competitor analyst. Execute only the instruction given.",
    service=chat_service,
)

trend_agent = ChatCompletionAgent(
    name="TrendAgent",
    description="Identifies emerging market trends and patterns.",
    instructions="You are a trend analyst. Execute only the instruction given.",
    service=chat_service,
)

# -----------------
# Agent selection
# -----------------
AGENTS = {
    "Orchestrator": orchestrator,
    "NewsAgent": news_agent,
    "CompetitorAgent": competitor_agent,
    "TrendAgent": trend_agent,
}
available_agents = [a for a in AGENTS.keys() if a != "Orchestrator"]

# -----------------
# Orchestrator instructions
# -----------------
orchestrator.instructions = (
    f"You are the Orchestrator. Always generate a JSON plan for the "
    f"'{target_industry}' industry.\n"
    f"- The 'title' must explicitly include '{target_industry}'.\n"
    f"- Each step description must also reference '{target_industry}'.\n"
    f"- You may ONLY assign tasks to these agents: {', '.join(available_agents)}.\n"
    f"- You may assign multiple steps to the same agent.\n"
    f"- You do not need to use all agents, but you must not use agents outside this list.\n"
    "After generating the plan, delegate each step to workers by prefixing with '@WorkerName'. "
    "Finally, after all worker replies, include a synthesis step '@Orchestrator' "
    "that combines their outputs into a final market analysis report."
)

# -----------------
# Tracking orchestration details
# -----------------
MAX_ITERATIONS = 6
iteration_count = 0
agents_used = set()
history = []

def track_response(msg: ChatMessageContent, runtime: InProcessRuntime = None) -> None:
    """Callback to track agent responses and handle max iterations."""
    global iteration_count
    iteration_count += 1
    agents_used.add(msg.name)
    history.append(msg)

    print(f"\n--- Iteration {iteration_count}: {msg.name} ---\n{msg.content}")

    # Stop early if max iterations reached
    if iteration_count >= MAX_ITERATIONS:
        print(f"\n[Manager] Reached maximum iteration limit ({MAX_ITERATIONS}). Stopping orchestration.\n")
        if runtime is not None:
            asyncio.create_task(runtime.stop_when_idle())

# -----------------
# Build orchestration
# -----------------
manager = StandardMagenticManager(chat_completion_service=chat_service)

orchestration = MagenticOrchestration(
    members=[orchestrator, news_agent, competitor_agent, trend_agent],
    manager=manager,
    agent_response_callback=lambda msg: track_response(msg, runtime=None),  # runtime injected later
)

# -----------------
# Run orchestration
# -----------------
async def main():
    global orchestration
    runtime = InProcessRuntime()
    runtime.start()

    # Inject runtime into callback
    orchestration.agent_response_callback = lambda msg: track_response(msg, runtime)

    # Phase 1: generate JSON plan
    plan_prompt = (
        f"Generate a market analysis plan for the target industry: {target_industry}. "
        f"The plan must only use these agents: {', '.join(available_agents)}.\n"
        "You may reuse an agent for multiple steps, and you don’t need to use them all.\n"
        "Format:\n"
        "{\n"
        f"  \"title\": \"Market analysis plan for the {target_industry} industry\",\n"
        "  \"steps\": [ ... ]\n"
        "}\n"
    )

    plan = ""
    async for msg in orchestrator.invoke(task=plan_prompt, runtime=runtime):
        plan += str(msg)

    print("\n=== Execution Plan ===")
    print(plan)

    # Phase 2: execute plan
    execution_prompt = (
        plan
        + "\n\nNow execute the above plan exactly as written. "
        "Use '----- @WorkerName -----' to assign each subtask, "
        "and finish with '@Orchestrator' synthesis."
    )

    orchestration_result = await orchestration.invoke(
        task=execution_prompt,
        runtime=runtime,
    )

    final_report = await orchestration_result.get()
    print("\n=== Final Aggregated Report ===\n")
    print(final_report)

    # -----------------
    # Print orchestration summary
    # -----------------
    unused_agents = set(available_agents) - agents_used
    print("\n=== Orchestration Summary ===")
    print(f"Total iterations: {iteration_count}")
    print(f"Agents used: {', '.join(agents_used) if agents_used else 'None'}")
    print(f"Agents not used: {', '.join(unused_agents) if unused_agents else 'None'}")
    if iteration_count >= MAX_ITERATIONS:
        print(f"Execution stopped early due to max iteration limit ({MAX_ITERATIONS}).")

    await runtime.stop_when_idle()

if __name__ == "__main__":
    print("\n=== Starting Market Analysis Orchestrator ===\n")
    asyncio.run(main())


