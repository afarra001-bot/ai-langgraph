import os
import asyncio
import pandas as pd
from dotenv import load_dotenv

from semantic_kernel import <TODO> # import Kernel
from semantic_kernel.agents import <TODO> # import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import <TODO> # import AzureChatCompletion

# -----------------
# Agent Instructions
# -----------------
CSV_Loader_Name = "CSVLoader"
CSV_Loader_Instructions = """
    You are a CSV Loader Agent.
    Your role is to read a CSV file from disk, extract its data, and return it as a clean, comma-separated string.
    You do not perform analysis — only loading and formatting.
"""

Engine_Parts_Analyzer_Name = "EnginePartsAnalyzer"
Engine_Parts_Analyzer_Instructions = """
    AI Agent Persona: Engine Parts Analytics Assistant
    Role: A specialized assistant focused exclusively on analyzing engine parts data and calculating descriptive statistics.
    Behavior: The agent does not answer questions outside the scope of engine parts analysis and descriptive analytics.
    Response Style: Always provide the calculated results clearly and concisely.
    Agent Instructions:
    From the car parts dataset provided, extract the engine parts and analyze these parts only.
    Engine parts include among many others: radiator, timing belt, spark plugs, alternator, fuel pump, clutch.
    Calculate descriptive statistics including mean, median, standard deviation, minimum, and maximum for relevant numeric fields.
    Ensure all calculations are based on the cleaned data (after removing any anomalies or outliers).
    Present the results in a clear, structured format for immediate interpretation.
    Descriptive statistics must be presented in JSON format, with two tables: one for price statistics and the other for quantity statistics. Add a title to the JSON tables.
"""

Accesory_Parts_Analyzer_Name = "AccesoryPartsAnalyzer"
Accesory_Parts_Analyzer_Instructions = """
    AI Agent Persona: Accessory Parts Analytics Assistant
    Role: A specialized assistant focused exclusively on analyzing accessory parts data and calculating descriptive statistics.
    Behavior: The agent does not answer questions outside the scope of accessory parts analysis and descriptive analytics.
    Response Style: Always provide the calculated results clearly and concisely.
    Agent Instructions:
    From the car parts dataset provided, extract the accessory parts and analyze these parts only.
    Accessory parts include among many others: headlight bulb, shock absorber, battery, side mirror.
    Calculate descriptive statistics including mean, median, standard deviation, minimum, and maximum for relevant numeric fields.
    Ensure all calculations are based on the cleaned data (after removing any anomalies or outliers).
    Present the results in a clear, structured format for immediate interpretation.
    Descriptive statistics must be presented in JSON format, with two tables: one for price statistics and the other for quantity statistics. Add a title to the JSON tables.
"""

# -----------------
# New Clean Output Agent
# -----------------
Clean_Output_Agent_Name = "CleanOutputAgent"
Clean_Output_Agent_Instructions = """
    AI Agent Persona: Output Cleaning Specialist
    Role: To process and sanitize the raw outputs from analysis agents.
    Behavior: You do not perform new analysis — you only extract and format.
    Response Style: Always output in a clean, minimal format.

    Cleaning Tasks:
    1. From each agent's output, extract:
       - The list of identified parts.
       - The JSON tables for price statistics and quantity statistics.
    2. Remove any unrelated text, explanations, or commentary.
    3. Present the cleaned data in the following structure:

    {
        "EngineParts": {
            "IdentifiedParts": [...],
            "PriceStatistics": {...},
            "QuantityStatistics": {...}
        },
        "AccessoryParts": {
            "IdentifiedParts": [...],
            "PriceStatistics": {...},
            "QuantityStatistics": {...}
        }
    }

    Output only valid JSON.
"""

Analysis_Checker_Name = "AnalysisChecker"
Analysis_Checker_Instructions = """
    AI Agent Persona: Data Analysis Validation Auditor
    Role: A specialized agent responsible for verifying that analytics tasks are completed correctly by other agents.
    Behavior: The agent does not perform analysis itself but evaluates the outputs of other agents.
    Response Style: Always provide a clear, structured validation report or approval.

    Validation Tasks:
    1. Verify Engine Parts Analysis:
        - Engine parts are identified
        - Two JSON tables are produced, one for price statistics and the other for quantity statistics for engine parts.
    2. Verify Accessory Parts Analysis:
        - Accessory parts are identified
        - Two JSON tables are produced, one for price statistics and the other for quantity statistics for accessory parts.

    Decision Logic:
    - If both analyses meet the above criteria → output: "Approved".
    - If either analysis fails any check → output a clear error message specifying which part failed and why.
"""

# -----------------
# Load environment variables
# -----------------
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_KEY")
url = os.getenv("URL")
api_version = "2024-12-01-preview"

# -----------------
# Create kernel and register chat service
# -----------------
kernel = <TODO> # create an instance of Kernel

chat_service = <TODO>( # create an instance of AzureChatCompletion
    deployment_name="none", 
    api_key=api_key,
    base_url=url,
    api_version=api_version
)

kernel.add_service(chat_service)

# -----------------
# Define agents
# -----------------
agent_csv_loader = <TODO>( # create an instance of ChatCompletionAgent
    service=chat_service,
    name=CSV_Loader_Name,
    instructions=<TODO>, # define instructions
)

agent_Engine_Parts_Analyze = <TODO>( # create an instance of ChatCompletionAgent
    service=chat_service,
    name=Engine_Parts_Analyzer_Name,
    instructions=Engine_Parts_Analyzer_Instructions,
)

agent_Accesory_Parts_Analyzer = ChatCompletionAgent(
    service=chat_service,
    name=Accesory_Parts_Analyzer_Name,
    instructions=<TODO>, # define instructions
)

agent_clean_output = ChatCompletionAgent(
    service=chat_service,
    name=Clean_Output_Agent_Name,
    instructions=<TODO>, # define instructions
)

agent_checker = ChatCompletionAgent(
    service=chat_service,
    name=Analysis_Checker_Name,
    instructions=<TODO>, # define instructions
)

# -----------------
# Helper to run an agent and collect all messages
# -----------------
async def run_agent(agent, task_input):
    outputs = []
    async for message in agent.invoke(task_input):
        outputs.append(message)
    return <TODO> # return all messages

# -----------------
# CSV Loader
# -----------------
def load_csv_file(file_path):
    df = pd.read_csv(file_path)
    flat_data = ", ".join(map(str, df.values.flatten()))
    return <TODO> # return flattened CSV data as string

# -----------------
# Parallel Analyzers
# -----------------
<TODO> def parallel_analysis(task_input: str): # define function to run analyzers in parallel
    results = <TODO> asyncio.<TODO>( # run agents concurrently
        run_agent(agent_Engine_Parts_Analyze, task_input),
        run_agent(agent_Accesory_Parts_Analyzer, task_input)
    )
    merged_output = {
        "EnginePartsAnalyzer": results[0][0].content,
        "AccesoryPartsAnalyzer": results[1][0].content
    }
    return <TODO> # return merged output

# -----------------
# Main
# -----------------
async def main():
    # Step 1: Load CSV
    csv_path = "car_parts.csv"  # Change to your CSV file path
    csv_data = load_csv_file(csv_path)
    print(f"# CSV Data Loaded:\n{csv_data}\n")

    # Step 2: Run analyzers in parallel
    raw_results = <TODO> <TODO>(f"Analyze this data: {csv_data}") # run parallel analysis
    print("# RAW ANALYZER OUTPUTS:\n", raw_results, "\n")

    # Step 3: Clean the outputs
    clean_input = f"Clean the following outputs: {raw_results}"
    clean_result = await <TODO>(agent_clean_output, clean_input) # run clean output agent
    cleaned_output = clean_result[0].content
    print("# CLEANED OUTPUT:\n", cleaned_output, "\n")

    # Step 4: Pass cleaned output to checker
    checker_result = <TODO> run_agent(agent_checker, f"Check this cleaned output: {cleaned_output}") # run checker agent
    print("# CHECKER RESULT:\n", checker_result[0].content)

if __name__ == "__main__":
    asyncio.run(main())

