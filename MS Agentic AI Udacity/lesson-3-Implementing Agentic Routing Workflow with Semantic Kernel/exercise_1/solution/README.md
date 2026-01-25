# Agent Routing Orchestration with Semantic Kernel 

## Learning Objectives
This exercise will help you understand how to build and orchestrate multiple specialized AI agents using Semantic Kernel:

- **The Kernel:** Central orchestration hub for AI services and agents

- **ChatCompletionAgent:** Domain‑specific conversational agents with strict behavioral rules

 - **Agent Orchestration:** Routing user requests to the correct specialized agent

- **Plugin Integration:** Passing other agents as callable plugins

- **Async Streaming:** Handling streamed responses from agents

## Exercise Overview
You will implement a **multi‑agent data analysis system** using Semantic Kernel. The system consists of:

- A **Data Cleaning Agent** that always responds with a fixed cleaning instruction

- A **Data Visualization** Agent that always responds with a fixed visualization instruction

- An **Orchestration Agent** that never answers directly but routes requests to the correct specialized agent

This demonstrates how to chain agents together and enforce strict domain boundaries.

## Requirements
### Prerequisites
- Python 3.8+

- Azure OpenAI account with a deployed chat model (e.g., GPT‑4 or GPT‑4.1‑mini)

- Basic understanding of async/await in Python

### Dependencies
Install the required packages:

- pip install semantic-kernel python-dotenv
- Environment Setup
  - Create a .env file in your project root with the following variables:

AZURE_OPENAI_KEY=your_azure_openai_api_key    
URL=your_azure_openai_endpoint_url

## Getting Started
- Download the starter code provided in this repository

- Review the agent definitions to understand their roles and restrictions

- Set up your environment with the required dependencies and .env file

- Run the code to see how the orchestration agent delegates requests

- Observe the output to verify that each request is routed to the correct agent

## Task Description
You are provided with a complete implementation of a multi‑agent orchestration pattern. The key components are:

### 1. Kernel Setup
Initialize a Kernel instance

- Configure and register an AzureChatCompletion service

- Use API version "2024-12-01-preview"

### 2. Specialized Agents
- **DataCleaningAgent:**

  - Only answers data cleaning questions

  - Always responds with: "Get rid of all outliers."

- **DataVisualizationAgent:**

  - Only answers data visualization questions

  - Always responds with: "You use matplotlib for plotting your data."

### 3. Orchestration Agent
- **OrchestrationAgent:**

  - Identifies the type of request

  - Routes to the correct specialized agent via plugin calls

  - Never answers directly

  - If no agent can handle the request, responds with: "I do not have analysts that can help with that"

### 4. Chat Thread
- Uses ChatHistoryAgentThread to maintain conversation history (not heavily used in this example but ready for extension)

### 5. Execution Flow
- Iterates over a list of prompts

- For each prompt:

  - Prints the prompt number and text

  - Invokes the orchestration agent

  - Streams and prints the agent’s response

## Testing and Validation
Run the script:

python your_script_name.py
You should see output similar to:

--------------------
1 - Running agent for prompt: How do I clean my data?
Agent says: Get rid of all outliers.

--------------------
2 - Running agent for prompt: How do I visualize my data?
Agent says: You use matplotlib for plotting your data.

--------------------
3 - Running agent for prompt: How do I do descriptive statistics on my data?
Agent says: I do not have analysts that can help with that

--------------------
4 - Running agent for prompt: How do I process Healthcare data
Agent says: I do not have analysts that can help with that

## Expected Behavior
- Data Cleaning Questions → Routed to DataCleaningAgent

- Data Visualization Questions → Routed to DataVisualizationAgent

- Other Questions → Orchestration agent declines with the fallback message

- Output Format → Each prompt is labeled and the response is prefixed with "Agent says:"

## Key Concepts to Demonstrate
### Kernel Architecture
- Centralized service registration

- Passing services to multiple agents

### Agent Specialization
- Strict domain boundaries enforced via instructions

- Fixed, predictable responses for testing

### Orchestration Pattern
- One agent managing and delegating to others

- Plugins as callable sub‑agents

### Async Operations
- Streaming responses with async for

- Event loop management with asyncio.run

## Success Criteria
Your solution should:

- Correctly initialize the kernel and register the Azure OpenAI service

- Create two specialized agents with fixed responses

- Implement an orchestration agent that routes requests appropriately

- Produce the expected output for all test prompts

- Use proper async patterns for agent invocation

## Architecture Notes
This exercise demonstrates:

- Multi‑Agent Collaboration: How agents can be composed into larger workflows

- Plugin‑Based Routing: Passing agents as callable plugins to another agent

- Strict Instruction Enforcement: Using prompt engineering to lock agent behavior

- Service Reuse: All agents share the same underlying Azure OpenAI service
