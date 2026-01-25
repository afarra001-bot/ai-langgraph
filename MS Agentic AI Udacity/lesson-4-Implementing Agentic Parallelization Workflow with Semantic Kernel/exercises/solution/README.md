# Agent Routing and Parallel Analysis with Semantic Kernel

## Learning Objectives

This exercise will help you understand how to build and orchestrate **multiple specialized AI agents running in parallel** using Semantic Kernel:

* **The Kernel:** Central orchestration hub for AI services and agents.
* **ChatCompletionAgent:** Domain‑specific conversational agents with strict behavioral rules.
* **Parallel Agent Execution:** Run multiple agents simultaneously on the same input data.
* **Agent Chaining:** Pass outputs from one agent to another for cleaning and validation.
* **Async Streaming:** Handle streamed responses from agents efficiently.

## Exercise Overview

You will implement a **multi‑agent data analysis system** using Semantic Kernel. The system consists of:

* A **CSV Loader Agent** that reads and flattens CSV data for analysis.
* Two **Specialized Analysis Agents** that perform domain-specific analytics:

  * Engine Parts Analyzer
  * Accessory Parts Analyzer
* A **Clean Output Agent** that sanitizes and structures the outputs from analysis agents.
* An **Analysis Checker Agent** that validates results and approves or flags errors.

This demonstrates how to **orchestrate agents in parallel** and chain their outputs through a validation workflow.

## Requirements

### Prerequisites

* Python 3.8+
* Azure OpenAI account with a deployed chat model (e.g., GPT‑4 or GPT‑4.1‑mini)
* Basic understanding of async/await in Python

### Dependencies

Install the required packages:

```bash
pip install semantic-kernel python-dotenv pandas
```

### Environment Setup

Create a `.env` file in your project root with the following variables:

```text
AZURE_OPENAI_KEY=your_azure_openai_api_key
URL=your_azure_openai_endpoint_url
```

## Getting Started

* Download the provided Python script.
* Review the agent definitions to understand their roles and instructions.
* Set up your environment with the required dependencies and `.env` file.
* Run the code to see how the two analyzers process data **in parallel**.
* Observe the cleaned and validated output from the pipeline.

## Task Description

You are provided with a complete implementation of a **parallel multi-agent orchestration pattern**. The key components are:

### 1. Kernel Setup

* Initialize a Kernel instance.
* Register an AzureChatCompletion service using API version `2024-12-01-preview`.
* All agents share this service for consistency.

### 2. Specialized Agents

* **CSVLoader Agent:**

  * Reads CSV files and flattens data into a single string.
  * Does **not perform analysis**.

* **EnginePartsAnalyzer Agent:**

  * Performs descriptive statistics on engine parts (e.g., radiator, spark plugs).
  * Outputs structured JSON tables for price and quantity.

* **AccessoryPartsAnalyzer Agent:**

  * Performs descriptive statistics on accessory parts (e.g., battery, headlights).
  * Outputs structured JSON tables for price and quantity.

### 3. Clean Output Agent

* Receives raw results from analyzers.
* Extracts only relevant parts and statistics.
* Outputs a clean, consistent JSON structure.

### 4. Analysis Checker Agent

* Validates outputs from analysis agents.
* Approves or flags errors if any required tables or parts are missing.

### 5. Parallel Execution

* Both analyzers (`EnginePartsAnalyzer` and `AccessoryPartsAnalyzer`) run **concurrently** using `asyncio.gather`.
* This demonstrates **parallel agent orchestration** in Semantic Kernel.

## Execution Flow

1. Load CSV data using `CSVLoader`.
2. Run **EnginePartsAnalyzer** and **AccessoryPartsAnalyzer** in parallel.
3. Merge the raw outputs.
4. Pass merged outputs to **Clean Output Agent**.
5. Validate cleaned outputs with **Analysis Checker Agent**.
6. Print the final approved or error message.

## Testing and Validation

Run the script:

```bash
python your_script_name.py
```

You should see output similar to:

```text
# CSV Data Loaded:
...

# RAW ANALYZER OUTPUTS:
{
  "EnginePartsAnalyzer": "...",
  "AccesoryPartsAnalyzer": "..."
}

# CLEANED OUTPUT:
{
  "EngineParts": {...},
  "AccessoryParts": {...}
}

# CHECKER RESULT:
Approved
```

## Expected Behavior

* Engine part questions → Routed to EnginePartsAnalyzer.
* Accessory part questions → Routed to AccessoryPartsAnalyzer.
* Clean outputs → JSON with structured tables.
* Final validation → "Approved" if all outputs are correct.

## Key Concepts to Demonstrate

### Kernel Architecture

* Centralized service registration.
* All agents share the same Azure OpenAI service.

### Agent Specialization

* Strict domain boundaries via instructions.
* Outputs restricted to numeric analyses and JSON formatting.

### Parallel Agent Pattern

* Multiple agents invoked concurrently.
* Async operations handled with `asyncio.gather`.

### Output Chaining

* Raw outputs → Clean Output Agent → Validation Agent.
* Demonstrates how to compose agents in workflows.

## Success Criteria

Your solution should:

* Initialize Kernel and register the Azure OpenAI service.
* Run two specialized analysis agents in parallel.
* Clean and validate outputs correctly.
* Produce structured JSON with descriptive statistics.
* Follow proper async patterns for agent invocation.

## Architecture Notes

This exercise demonstrates:

* **Multi-Agent Collaboration:** Agents performing complementary tasks.
* **Parallel Execution:** Concurrent processing of independent analysis tasks.
* **Strict Instruction Enforcement:** Locking behavior via prompt engineering.
* **Service Reuse:** All agents share the same underlying Azure OpenAI service.
