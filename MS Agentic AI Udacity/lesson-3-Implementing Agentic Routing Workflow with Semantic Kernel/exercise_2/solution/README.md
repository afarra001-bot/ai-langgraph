# Data Analysis Agent System with Semantic Kernel Functions

## Learning Objectives
This exercise will help you understand how to build a data analysis orchestration system with Semantic Kernel using **plugins and function calling**. You will learn how to:

- **Kernel Setup**: Initialize a Semantic Kernel instance with Azure OpenAI  
- **Plugin Functions**: Implement specialized data analysis plugins (outlier removal, missing data handling, visualization)  
- **Orchestration Agent**: Use a central ChatCompletionAgent to route user queries to the right plugin  
- **Function Calling**: Ensure correct invocation of specialized plugin methods  
- **Async Operations**: Handle streamed agent responses with `async for`  

---

## Exercise Overview
You will implement a **multi-plugin agent system** for data analysis. The system consists of:

- **Outlier Removal Plugin** – general guidance on removing outliers  
- **Outlier Detection Executor Plugin** – executes actual outlier detection on numerical data  
- **Missing Data Plugin** – provides strategies for imputing missing values  
- **Data Visualization Plugin** – provides guidance on plotting and visualization tools  
- **Orchestrator Agent** – manages queries and routes them to the correct plugin function  

This demonstrates how to combine **rule-based orchestration** with **Semantic Kernel function calling**.

---

## Requirements

### Prerequisites
- Python 3.8+  
- Azure OpenAI account with a deployed chat model (e.g., GPT-4 or GPT-4.1-mini)  
- Basic knowledge of statistical methods (outliers, missing data)  
- Familiarity with async/await in Python  

### Dependencies
Install the required packages:

pip install semantic-kernel python-dotenv numpy

### Environment Setup

Create a .env file in your project root with the following variables:

AZURE_OPENAI_KEY=your_azure_openai_api_key
URL=your_azure_openai_endpoint_url

### Getting Started

- Install required dependencies

- Configure your .env with Azure OpenAI credentials

- Run the script

### Task Description

You are provided with an orchestration system containing the following components:

### 1. Kernel Setup
- Initializes a Kernel instance

- Registers an AzureChatCompletion service with API version 2024-12-01-preview

### 2. Plugin Implementations
- OutlierRemovalPlugin → General guidance using IQR/Z-score

- MissingDataPlugin → Imputation methods for missing values

- OutlierDetectionExecutorPlugin → Extracts numbers and applies IQR & Z-score detection

- DataVisualizationPlugin → Provides plotting advice (matplotlib)

### 3. Orchestrator Agent
- Uses ChatCompletionAgent with instructions

- Routes user queries to correct plugin functions

- Enforces rules:

  - Actual numbers → execute_outlier_removal

  - Outlier questions without numbers → remove_outliers

  - Missing data → handle_missing_data

  - Visualization → visualize_data

  - General cleaning → clean_data_comprehensive

  - Other topics → politely decline

### 4. Execution Flow
- Iterates through test prompts

- Streams agent responses asynchronously

- Prints which function was invoked and the results

## Testing and Validation

Run the script and you should see results like:

```
============================================================
 Data Analysis Agent System with Semantic Kernel Functions
============================================================
 Available Functions:
   • remove_outliers - General outlier removal guidance
   • execute_outlier_removal - Process actual numerical data
   • handle_missing_data - Missing data handling
   • visualize_data - Data visualization guidance
   • clean_data_comprehensive - Comprehensive cleaning
============================================================

------------------------------------------------------------
Query 1: Remove outliers from this data: [1, 100, 6]
------------------------------------------------------------
 FUNCTION CALLED: execute_outlier_removal (Processing actual data)
 Agent Response: **Outlier Detection Results** ...
```

## Expected Behavior

- Outlier Guidance → Uses remove_outliers

- Actual Data with Numbers → Uses execute_outlier_removal

- Missing Data → Uses handle_missing_data

- Visualization → Uses visualize_data

- Other Queries → Orchestrator politely declines

**Output Format** → Each query shows the function invoked and the agent response.

## Key Concepts to Demonstrate
- Kernel Architecture: Service registration and plugin injection

- Function Calling: Explicit plugin methods instead of generic responses

- Agent Specialization: Each plugin handles only its domain

- Orchestration Pattern: Central agent routes to specialized plugins

- Async Streaming: Agent responses streamed incrementally

## Success Criteria

Your solution should:

- Correctly initialize the kernel and Azure service

- Implement all plugins with appropriate responses

- Route requests through the orchestrator agent according to rules

- Process numerical data with both IQR and Z-score methods

- Produce consistent responses for all test prompts

## Architecture Notes

This exercise demonstrates:

- Plugin-Based Orchestration – managing specialized functions

- Instruction Enforcement – ensuring the agent always delegates correctly

- Multi-Agent Collaboration – orchestrator + specialized plugins

- Reusable Services – all plugins share the same Azure OpenAI service
