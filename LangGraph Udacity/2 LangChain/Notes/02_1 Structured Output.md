# Structured Output in LangChain - Summary

Based on your notebook, structured output in LangChain allows you to transform unstructured LLM responses into typed, validated data structures.

## Core Concept

**`llm.with_structured_output(schema)`** creates an LLM that returns data conforming to a specific schema instead of raw text.

## Two Approaches for Defining Schemas

### 1. **TypedDict** (Simpler)
````python
from typing_extensions import Annotated, TypedDict

class UserInfo(TypedDict):
    """User's info."""
    name: Annotated[str, "", "User's name. Defaults to ''"]
    country: Annotated[str, "", "Where the user lives. Defaults to ''"]

llm_with_structure = llm.with_structured_output(UserInfo)
response = llm_with_structure.invoke("My name is Henrique, and I am from Brazil")
# Returns: {'name': 'Henrique', 'country': 'Brazil'}
````

### 2. **Pydantic BaseModel** (More Powerful)
````python
from pydantic import BaseModel, Field

class PydanticUserInfo(BaseModel):
    """User's info."""
    name: Annotated[str, Field(description="User's name", default=None)]
    country: Annotated[str, Field(description="Where user lives", default=None)]

llm_with_structure = llm.with_structured_output(PydanticUserInfo)
response = llm_with_structure.invoke("I'm from Australia")
# Returns Pydantic object: PydanticUserInfo(name=None, country='Australia')
````

## Output Parsers (For Post-Processing)

### Basic Parsers
- **StrOutputParser**: Extracts plain text
- **DatetimeOutputParser**: Converts to datetime objects
- **BooleanOutputParser**: Converts to boolean
- **PydanticOutputParser**: Validates against Pydantic schema

### Self-Healing Parser (The Smart One!)
````python
# Regular parser fails on malformed output
parser = PydanticOutputParser(pydantic_object=Performer)

# Smart parser uses LLM to fix formatting errors
smart_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

# Handles malformed JSON like {'name': 'value'} instead of {"name": "value"}
response = smart_parser.parse(misformatted_result)
````

## Key Benefits

1. **Type Safety**: Get Python objects instead of strings
2. **Validation**: Automatic schema validation
3. **Error Recovery**: `OutputFixingParser` can auto-correct malformed output
4. **Consistency**: Guaranteed data structure across all responses
5. **Developer Experience**: IDE autocomplete and type checking

## When to Use What

- **TypedDict**: Quick prototypes, simple data extraction
- **Pydantic**: Production code, complex validation, nested structures
- **OutputFixingParser**: When dealing with unreliable formatting from LLMs

The structured output feature essentially turns your LLM into a typed API!