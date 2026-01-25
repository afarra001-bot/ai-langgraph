# Semantic Kernel Multi‑Agent Safety & Operations Planner

## Learning Objectives

This exercise will help you understand how to build specialized, chained agents with Semantic Kernel that collaboratively produce a complex, multi‑domain plan. You will explore:

- **The Kernel** — the central hub for registering and managing AI services and plugins
- **ChatCompletionAgents** — role‑specific AI agents with tailored instructions and execution settings
- **Plugin Integration** — enabling agents to call external functions (e.g., weather forecast)
- **Chained Execution** — passing evolving context from one agent to the next
- **Async streaming** — handling incremental responses from each agent

## Exercise Overview

You will implement four specialized agents — Safety Engineer, Regulation Expert, Weather Adaptation Specialist, and Final Integration Manager — all powered by Semantic Kernel and sharing the same Azure OpenAI service.

Instead of answering independently, these agents work sequentially:

1. **SafetyAgent** — drafts a baseline safety plan for a hydrocarbon processing plant
2. **RegulationAgent** — integrates OSHA, EPA, and API/NFPA compliance requirements
3. **WeatherAgent** — adapts the plan for forecasted weather conditions using a weather plugin
4. **FinalIntegrationAgent** — merges all sections into a coherent, final service plan

This demonstrates multi‑agent orchestration where each agent builds on the previous output.

## Requirements

### Prerequisites

- Python 3.8+
- Azure OpenAI account with a gpt‑4.1‑mini deployment
- Basic understanding of Python's async/await

### Dependencies

Install the required packages:

```bash
pip install semantic-kernel python-dotenv
```

### Environment Setup

Create a `.env` file in your project root with:

```
AZURE_OPENAI_KEY=your_azure_openai_api_key
URL=your_azure_openai_endpoint_url
```

## Getting Started

1. **Download the starter code** provided by your instructor
2. **Review the `<TODO>` comments** throughout the code - these mark the sections you need to complete
3. **Set up your environment** with the required dependencies and `.env` file
4. **Complete each `<TODO>` section** following the guidance in the comments
5. **Run your completed code** and verify that the testing scenarios produce the expected behavior
6. **Analyze the output** to ensure all agents work correctly in the chain

## Task Description

You are provided with starter code containing `<TODO>` comments that guide you through the implementation. Your task is to **complete all the `<TODO>` sections** to create a multi-agent system with the following specifications:

### 1. Kernel Setup
- `<TODO>`: Initialize a Semantic Kernel instance
- `<TODO>`: Configure and register an Azure OpenAI chat completion service
- `<TODO>`: Use deployment gpt-4.1-mini with API version 2024-12-01-preview

### 2. Weather Plugin Implementation
- `<TODO>`: Define a WeatherPlugin class with a search function
- `<TODO>`: Use @kernel_function so agents can call it natively
- `<TODO>`: Return simulated weather data (can be replaced with a real API)

### 3. Multi-Agent Configuration
Create four ChatCompletionAgents with specific roles and settings:

#### SafetyAgent
- `<TODO>`: Set temperature to 0.3 for deterministic, standards-aligned safety plans
- `<TODO>`: Configure role-specific instructions for baseline safety planning

#### RegulationAgent
- `<TODO>`: Set temperature to 0.35 to merge multiple regulatory frameworks
- `<TODO>`: Configure instructions to integrate OSHA, EPA, and API/NFPA compliance

#### WeatherAgent
- `<TODO>`: Set temperature to 0.55 for creative adaptation to weather scenarios
- `<TODO>`: Configure instructions to adapt plans based on weather plugin data

#### FinalIntegrationAgent
- `<TODO>`: Set temperature to 0.7 for narrative flow and integration
- `<TODO>`: Configure instructions to merge all sections into coherent final plan

### 4. Chain Execution Implementation
- `<TODO>`: Start with an initial prompt describing the task and location
- `<TODO>`: Pass the evolving current_output from one agent to the next
- `<TODO>`: Stream each agent's output asynchronously
- `<TODO>`: Print the final integrated service plan

## Testing Scenarios

Complete the implementation by filling in all `<TODO>` sections, then test with these variations:

1. **Location Testing**: Change location to "Gulf Coast refinery" vs "Mountain facility" to test different weather forecasts
2. **Temperature Adjustment**: Modify temperature values to see how creativity vs. determinism affects output
3. **Weather Integration**: Ensure WeatherAgent successfully calls the WeatherPlugin
4. **Chain Validation**: Verify each agent builds on the previous agent's output
5. **Final Integration**: Confirm the final plan is coherent and well-structured

## Expected Behavior

After completing all `<TODO>` sections, your program should demonstrate:

- **Sequential enrichment** — each agent builds on the previous agent's output
- **Plugin usage** — WeatherAgent calls the WeatherPlugin to adapt the plan
- **Role fidelity** — each agent stays within its domain of expertise
- **Final integration** — coherent, well‑structured service plan at the end
- **Output Format**: Each agent's response should be clearly labeled with streaming output

## Key Concepts to Demonstrate

### Kernel Architecture
- How the Kernel serves as the central coordination point for AI services and plugins
- Service registration and management across multiple agents
- Shared kernel instance across multiple agents

### Agent Specialization
- Role‑specific instructions and execution settings
- Temperature tuning for precision vs. creativity
- Domain expertise boundaries

### Plugin Integration
- Using @kernel_function to expose Python functions to agents
- Allowing agents to autonomously invoke plugins
- Dynamic plan modification based on external data

### Async Operations
- Streaming responses from each agent
- Sequential chaining while preserving intermediate outputs
- Proper use of async/await for SK operations

## Success Criteria

Your solution should:

1. **Complete all `<TODO>` sections** in the provided starter code
2. Initialize a Semantic Kernel with Azure OpenAI service
3. Register and use a weather plugin successfully
4. Create four specialized agents with clear, distinct roles
5. **Demonstrate that all testing scenarios behave as expected**:
   - Each agent contributes meaningfully to the evolving plan
   - Weather data is successfully integrated into the plan
   - Final output is a coherent, comprehensive service plan
6. Pass evolving context through the agent chain correctly
7. Stream and display each agent's output with proper formatting
8. Show clear understanding of multi-agent orchestration patterns

## Architecture Notes

This exercise demonstrates several key Semantic Kernel concepts:

- **Service‑Oriented Design** — one AI service powering multiple agents
- **Agent Chain Pattern** — sequential role‑based processing
- **Execution Settings** — fine‑tuning temperature and token limits per agent
- **Plugin‑Driven Adaptation** — dynamic plan modification based on external data
- **Multi-Agent Orchestration** — coordinated execution of specialized AI agents

Understanding these patterns will prepare you to build scalable, domain‑specialized, multi‑agent AI systems with Semantic Kernel.