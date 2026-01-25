# Combining Chat History and Prompt Templates

You can combine chat history (list of LangChain message objects) with prompt templates by using **ChatPromptTemplate** instead of `PromptTemplate`. Here's how:

## Method 1: Using ChatPromptTemplate

````python
from langchain_core.prompts import ChatPromptTemplate

# Create a chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a geography tutor"),
    ("human", "What's the capital of Brazil?"),
    ("ai", "The capital of Brazil is Brasília"),
    ("human", "{user_question}")  # Variable for new question
])

# Invoke with the template
response = llm.invoke(chat_prompt.invoke({"user_question": "What's the capital of Canada?"}))
print(response.content)
````

## Method 2: Manually Combining Lists

You can also build the message list dynamically and append formatted prompts:

````python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Existing chat history
chat_history = [
    SystemMessage("You are a geography tutor"),
    HumanMessage("What's the capital of Brazil?"),
    AIMessage("The capital of Brazil is Brasília")
]

# Create a prompt template for the new question
prompt_template = PromptTemplate(template="What's the capital of {country}?")

# Add the formatted prompt as a new HumanMessage
new_question = HumanMessage(prompt_template.format(country="Canada"))
messages = chat_history + [new_question]

# Invoke with the combined list
response = llm.invoke(messages)
print(response.content)
````

## Method 3: Using MessagesPlaceholder

For more complex scenarios with variable-length chat history:

````python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])

# Pass both history and new input
response = llm.invoke(chat_prompt.invoke({
    "role": "geography tutor",
    "chat_history": [
        HumanMessage("What's the capital of Brazil?"),
        AIMessage("The capital of Brazil is Brasília")
    ],
    "user_input": "What about Canada?"
}))
print(response.content)
````

**Key Insight**: `ChatPromptTemplate` is designed for conversational contexts, while `PromptTemplate` is for simple string templates. Use `ChatPromptTemplate` when working with message-based chat histories.