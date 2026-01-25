# Creator–Critic SOP Orchestrator with Semantic Kernel

## Learning Objectives

This exercise will help you understand how to **implement a multi-agent creator–critic pattern** using Semantic Kernel. Specifically, you will learn:

* **The Kernel:** Central orchestration hub for AI services and agents.  
* **ChatCompletionAgent:** Role-specific agents with tightly scoped instructions.  
* **Sequential Orchestration:** Agents invoked in order to create and refine outputs.  
* **Creator–Critic Loop:** A recursive review cycle where the Critic enforces strict approval criteria.  
* **Termination Control:** The loop runs until the output is explicitly approved or a maximum iteration count is reached.  

## Exercise Overview

You will implement a **document creation and review system** for industrial Standard Operating Procedures (SOPs). The workflow uses **two specialized agents**:  

* **CreatorAgent:** Drafts a complete SOP for a specified industrial task.  
* **CriticAgent:** Reviews the SOP against safety, compliance, and formatting rules.  

The system uses **Sequential Orchestration** to execute the Creator and Critic in sequence, repeating the cycle until the SOP is marked as **APPROVED** or the maximum iterations are reached.  

This demonstrates how to **build a recursive creator–critic workflow** where iterative feedback improves quality until standards are satisfied.  

## Requirements

### Prerequisites

* Python 3.8+  
* Azure OpenAI account with a deployed chat model (e.g., GPT-4 or GPT-4.1-mini)  
* Familiarity with async/await in Python  

### Dependencies

Install the required packages:

```
pip install semantic-kernel python-dotenv
```

## Environment Setup
Create a `.env` file in your project root with the following variables:

```
AZURE_OPENAI_KEY=your_azure_openai_api_key
URL=your_azure_openai_endpoint_url
```

## Starter Code
You will be provided with a starter Python script containing the orchestration skeleton.
In this script, several parts are marked with `<TODO>`.

Your task is to replace each `<TODO>` with the correct code to complete the corresponding step.
Examples of what you will implement include:

- Initializing the Kernel and AzureChatCompletion service.

- Defining the CreatorAgent and CriticAgent with their role-specific instructions.

- Implementing the Sequential Orchestration that connects the two agents.

- Writing the recursive loop that runs until the SOP is approved.

By completing all `<TODO>` sections, you will have a fully functional Creator–Critic SOP Orchestrator.

## Getting Started
1. Download the provided starter script.

2. Replace all `<TODO>` markers with the appropriate code.

3. Set the initial_task variable to the industrial operation you want an SOP for.

4. Run the script to watch the SOP evolve through creator–critic iterations until it is approved.

## Task Description
The key components of this orchestration pattern are:

**1. Kernel and Service Setup**
- Initialize a Kernel instance.
- Register an AzureChatCompletion service (API version: 2024-12-01-preview).
- Both Creator and Critic agents share this service for consistency.

**2. Specialized Agents**.  

**CreatorAgent:**

- Drafts a Standard Operating Procedure (SOP).
- Uses a clear numbered step format.
- Incorporates technical details when relevant.
- Revises the SOP if the Critic provides feedback with the REVISE label.

**CriticAgent:**

- Reviews the SOP strictly for format, safety, and compliance.
- Requires each step to include Action, Responsible Party, Safety Considerations, and Tools/Equipment Needed.
- If valid, responds with APPROVED and shows the final SOP.
- If not valid, provides feedback and appends the REVISE label, returning the original SOP for context.

**3. Sequential Orchestration**.  
- The Creator produces a draft SOP.
- The Critic evaluates and either approves or sends it back for revision.
- A recursive loop continues until approval or until MAX_ITERATIONS is reached.

**4. Execution Flow**.    
- Load environment variables.
- Initialize the Creator and Critic agents.
- Run a sequential orchestration loop:
- Creator drafts → Critic reviews → repeat if not approved.
- Stop once APPROVED is returned or 10 iterations have been completed.
- Print the final SOP and summary.

## Testing and Validation
Run the script:

```
python your_script_name.py
```
Example output:

```
=== Starting Document Creator-Critic Orchestrator ===

=== Iteration 1 ===
--- Current Task ---
Restarting a Gas Turbine after a Shutdown for Maintenance

--- Final Report ---
[Critic feedback with REVISE label]

=== SOP Requires Revision ===

=== Iteration 2 ===
--- Current Task ---
[Creator’s revised SOP draft]

--- Final Report ---
APPROVED
1. Verify turbine shutdown status...
2. Inspect inlet guide vanes...
...

=== SOP Approved ===
```

## Expected Behavior
- The CreatorAgent generates or revises an SOP each iteration.
- The CriticAgent enforces compliance with strict rules.
- The loop continues until the SOP is APPROVED or iterations are exhausted.
- The final SOP is a structured, safe, and compliant procedure.

## Key Concepts to Demonstrate
**Creator–Critic Pattern**    
- **CreatorAgent:** Produces content (SOP draft).
- **CriticAgent:** Enforces rules and provides revision feedback.
- **Recursive loop:** Iterates until content meets standards.

**Sequential Orchestration**.    
- Agents execute in sequence with shared state across iterations.
- Critic’s feedback feeds directly into Creator’s next draft.

**Instruction Enforcement**.   
- Both agents follow strict, role-specific instructions.
- Critic ensures only properly formatted SOPs are approved.

**Termination Conditions**.    
- Approval explicitly signaled with "APPROVED".
- Fallback termination after 10 iterations.

**Success Criteria**

Your solution should:
- Initialize Kernel and Azure OpenAI service.
- Run Creator and Critic in sequence.
- Track feedback and revisions across iterations.
- Produce a final approved SOP or terminate gracefully after max iterations.

**Architecture Notes**.   

This exercise demonstrates:
- Recursive Multi-Agent Workflows: Agents collaborate in iterative cycles.
- Creator–Critic Validation: Output only accepted when it passes strict review.
- Service Reuse: Shared Azure OpenAI chat completion service across agents.
- Sequential Orchestration: Simple and effective agent control flow.
- Industrial Relevance: SOP generation for real-world operational safety.