# Prompt Templates in LangChain

Prompt templates in LangChain are structured ways to create reusable prompts for LLMs. They help you:

## Key Types

### 1. **PromptTemplate**
Basic string-based template with placeholders.

````python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}"
)
prompt = template.invoke({"adjective": "funny", "content": "chickens"})
````

### 2. **ChatPromptTemplate**
For chat models with different message roles (system, human, AI).

````python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant named {name}"),
    ("human", "{user_input}")
])
````

### 3. **FewShotPromptTemplate**
Includes examples to guide the model's responses (as shown in your notebook).

````python
from langchain_core.prompts import FewShotPromptTemplate

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=[
        {"input": "Hi", "output": "Hello!"},
        {"input": "Bye", "output": "Goodbye!"}
    ]
)
````

## Benefits

- **Reusability**: Define once, use multiple times
- **Consistency**: Standardized prompt structure
- **Flexibility**: Easy to modify behavior through variables
- **Few-Shot Learning**: Guide model behavior with examples

In your notebook, the `ChatBot` class uses `FewShotChatMessagePromptTemplate` to give BEEP-42 its robotic personality through examples.


/n
/n

# Combining Different Prompt Templates

You can combine different types of prompt templates in LangChain to create sophisticated multi-purpose prompts. Here are the main approaches:

## 1. **Combining FewShot + Chat Prompts (Your Current Example)**

Your notebook already demonstrates this! You combine system instructions with few-shot examples:

````python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Define few-shot examples
examples = [
    {"input": "Hello!", "output": "BEEP. GREETINGS!"},
    {"input": "What is 2+2?", "output": "CALCULATING... RESULT: 4"}
]

# Create example template
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

# Create few-shot template
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

# Combine with system message and dynamic input
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are BEEP-42, a robotic assistant."),
    few_shot_prompt,  # Insert few-shot examples here
    ("human", "{user_input}")  # Dynamic user input
])

# Use it
messages = final_prompt.invoke({"user_input": "Tell me a joke"})
````

## 2. **Combining Multiple Prompt Templates with PipelinePrompt**

Chain multiple templates together sequentially:

````python
from langchain_core.prompts import PipelinePromptTemplate, PromptTemplate

# Template 1: Context setting
context_template = PromptTemplate.from_template(
    "You are analyzing data for: {domain}\nYour expertise level: {expertise}"
)

# Template 2: Task definition
task_template = PromptTemplate.from_template(
    "Task: {task_description}\nConstraints: {constraints}"
)

# Template 3: Output format
output_template = PromptTemplate.from_template(
    "Provide response in {format} format with {detail_level} detail."
)

# Combine into pipeline
final_template = PromptTemplate.from_template(
    "{context}\n\n{task}\n\n{output}\n\nQuestion: {question}"
)

pipeline = PipelinePromptTemplate(
    final_prompt=final_template,
    pipeline_prompts=[
        ("context", context_template),
        ("task", task_template),
        ("output", output_template)
    ]
)

# Invoke with all variables
result = pipeline.invoke({
    "domain": "healthcare",
    "expertise": "expert",
    "task_description": "Analyze patient data",
    "constraints": "HIPAA compliant",
    "format": "JSON",
    "detail_level": "high",
    "question": "What are the trends?"
})
````

## 3. **Conditional Template Selection**

Use different templates based on context:

````python
from langchain_core.prompts import ChatPromptTemplate

class AdaptiveChatBot:
    def __init__(self):
        # Define different personalities
        self.personalities = {
            "robot": ChatPromptTemplate.from_messages([
                ("system", "BEEP BOOP. You are a robot."),
                ("human", "{input}")
            ]),
            "professional": ChatPromptTemplate.from_messages([
                ("system", "You are a professional business assistant."),
                ("human", "{input}")
            ]),
            "casual": ChatPromptTemplate.from_messages([
                ("system", "You're a friendly, casual chatbot."),
                ("human", "{input}")
            ])
        }
    
    def get_response(self, user_input: str, personality: str):
        template = self.personalities.get(personality, self.personalities["casual"])
        return template.invoke({"input": user_input})

# Usage
bot = AdaptiveChatBot()
bot.get_response("Hello!", personality="robot")
````

## 4. **Nested Templates with Dynamic Content**

Combine static and dynamic content:

````python
from langchain_core.prompts import ChatPromptTemplate

# Create base template with nested structures
complex_template = ChatPromptTemplate.from_messages([
    ("system", """You are {bot_name}, a {bot_type} assistant.
    
Core Capabilities:
{capabilities}

Communication Style:
{style_guide}
"""),
    ("human", "{history}"),  # Conversation history
    ("human", "{user_input}")  # Current input
])

# Invoke with nested content
response = complex_template.invoke({
    "bot_name": "BEEP-42",
    "bot_type": "robotic",
    "capabilities": "- Math\n- Logic\n- Humor",
    "style_guide": "Use BEEP and BOOP sounds",
    "history": "Previous: What is 2+2? Answer: 4",
    "user_input": "Tell me more"
})
````

## 5. **Template Composition with Partial Variables**

Pre-fill some variables, leave others dynamic:

````python
from langchain_core.prompts import PromptTemplate

# Base template with partial variables
base_template = PromptTemplate(
    template="You are {name}, a {role}. {task}",
    input_variables=["task"],
    partial_variables={
        "name": "BEEP-42",
        "role": "robotic assistant"
    }
)

# Only need to provide 'task' when invoking
base_template.invoke({"task": "Explain quantum computing"})
````

## Key Benefits

- **Modularity**: Reuse components across different scenarios
- **Flexibility**: Switch behaviors without rewriting code
- **Maintainability**: Update one template affects all uses
- **Scalability**: Easy to add new personalities or contexts

The approach in your notebook (combining FewShot + Chat templates) is perfect for creating personality-driven chatbots!