# Market Analysis Orchestrator with Semantic Kernel

## Learning Objectives

This exercise will help you understand how to **build and orchestrate multiple specialized AI agents in a workflow** using Semantic Kernel:

* **The Kernel:** Central orchestration hub for AI services and agents.
* **ChatCompletionAgent:** Domain‑specific conversational agents with strict behavioral rules.
* **Orchestration:** Sequential and delegated execution of tasks across agents.
* **Agent Synthesis:** Combine outputs from multiple agents into a final report.
* **Async Streaming:** Handle streamed responses from agents efficiently.

## Exercise Overview

You will implement a **multi-agent market analysis system** using Semantic Kernel. The system consists of:

* A **Orchestrator Agent** that generates a JSON plan for executing the analysis and delegates tasks to other agents.
* Three **Specialized Worker Agents**:

  * **NewsAgent:** Gathers and summarizes recent market news.
  * **CompetitorAgent:** Analyzes competitors' strategies and performance.
  * **TrendAgent:** Identifies emerging market trends and patterns.

This demonstrates how to **orchestrate agents** where the orchestrator assigns tasks, tracks progress, and synthesizes the final market report.

## Requirements

### Prerequisites

* Python 3.8+
* Azure OpenAI account with a deployed chat model (e.g., GPT-4 or GPT-4.1‑mini)
* Basic understanding of async/await in Python

### Dependencies

Install the required packages:

```bash
pip install semantic-kernel python-dotenv
```

## Environment Setup

Create a `.env` file in your project root with the following variables:

```
AZURE_OPENAI_KEY=your_azure_openai_api_key
URL=your_azure_openai_endpoint_url
```

## Getting Started

1. Download the provided Python script.
2. Review the agent definitions to understand their roles and instructions.
3. Set the `target_industry` variable to the market you want to analyze.
4. Run the code to see how the orchestrator generates a plan, delegates tasks, and aggregates results from worker agents.

## Task Description

You are provided with a complete implementation of a market analysis orchestration pattern. The key components are:

### 1. Kernel and Service Setup

* Initialize a Kernel instance.
* Register an AzureChatCompletion service using API version 2024-12-01-preview.
* All agents share this service for consistency.

### 2. Specialized Agents

**Orchestrator Agent:**
* Generates a JSON plan for market analysis.
* Assigns tasks only to available worker agents.
* Combines all worker outputs into a final market report.

**NewsAgent:**
* Collects recent market news.
* Summarizes key points relevant to the target industry.

**CompetitorAgent:**
* Analyzes competitors' strategies, strengths, and weaknesses.
* Provides structured insights.

**TrendAgent:**
* Detects emerging trends and patterns.
* Highlights opportunities or risks for the industry.

### 3. Tracking and Iteration

* Responses from each agent are tracked.
* Maximum iteration count (MAX_ITERATIONS) prevents infinite loops.
* Summary statistics are generated, including which agents were used or unused.

### 4. Orchestration Pattern

* The Orchestrator agent generates a plan in JSON format.
* Worker agents execute assigned steps.
* Final synthesis is performed by the Orchestrator combining all worker outputs.

## Execution Flow

1. Load environment variables and initialize agents.
2. Orchestrator generates a JSON execution plan.
3. Worker agents execute assigned tasks concurrently in the orchestration.
4. Orchestrator synthesizes the final market report.
5. Print orchestration summary showing agent usage and iteration count.

## Testing and Validation

Run the script:

```bash
python your_script_name.py
```

You should see output similar to:

```
=== Starting Market Analysis Orchestrator ===

=== Execution Plan ===
{
  "title": "Market analysis plan for the aviation industry",
  "steps": [...]
}

--- Iteration 1: NewsAgent ---
...

--- Iteration 2: CompetitorAgent ---
...

=== Final Aggregated Report ===
...

=== Orchestration Summary ===
Total iterations: 4
Agents used: NewsAgent, CompetitorAgent, TrendAgent
Agents not used: None
```

## Expected Behavior

* Orchestrator generates a JSON plan with all steps labeled for specific agents.
* Worker agents execute tasks according to the plan.
* Outputs are synthesized into a structured final report.
* Iteration tracking ensures the system stops if MAX_ITERATIONS is reached.

## Key Concepts to Demonstrate

### Kernel Architecture
* Centralized service registration.
* Shared Azure OpenAI service across all agents.

### Agent Specialization
* Strict task boundaries enforced via instructions.
* Outputs are structured and specific to the assigned role.

### Orchestration Pattern
* Orchestrator plans tasks for workers.
* Worker agents execute tasks and return results.
* Final synthesis consolidates outputs into a coherent report.

### Async Streaming
* Handles streamed outputs efficiently.
* Allows step-by-step tracking and debugging.

## Success Criteria

Your solution should:

* Initialize the Kernel and register the Azure OpenAI service.
* Run worker agents according to the orchestrator plan.
* Track responses, iterations, and agent usage.
* Produce a final, structured market analysis report.
* Stop execution gracefully if maximum iterations are reached.

## Architecture Notes

This exercise demonstrates:

* **Multi-Agent Collaboration:** Agents performing complementary tasks.
* **Orchestration Control:** Orchestrator manages planning, delegation, and synthesis.
* **Strict Instruction Enforcement:** Agents follow assigned roles strictly.
* **Service Reuse:** All agents share the same underlying Azure OpenAI service.
* **Async Execution:** Ensures non-blocking execution and real-time tracking.