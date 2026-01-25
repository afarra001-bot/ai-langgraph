# Validating and Fixing Structured LLM Output

Here are the main approaches to validate and fix structured output from LLMs in LangChain:

## 1. **Built-in Pydantic Validation**

Pydantic automatically validates when creating objects:

````python
from pydantic import BaseModel, Field, validator, field_validator
from typing import List

class Performer(BaseModel):
    """Filmography info with validation"""
    name: str = Field(description="Actor/actress name", min_length=1)
    film_names: List[str] = Field(description="List of films", min_length=1)
    age: int = Field(description="Age", ge=0, le=150)
    rating: float = Field(description="Rating", ge=0.0, le=10.0)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or v.isspace():
            raise ValueError("Name cannot be empty")
        return v.strip().title()
    
    @field_validator('film_names')
    @classmethod
    def validate_films(cls, v):
        if not v:
            raise ValueError("Must have at least one film")
        return [film.strip() for film in v if film.strip()]

# If LLM returns invalid data, Pydantic raises ValidationError
llm_with_structure = llm.with_structured_output(Performer)
try:
    response = llm_with_structure.invoke("Generate info")
except Exception as e:
    print(f"Validation failed: {e}")
````

## 2. **OutputFixingParser for Malformed Strings**

When you have string data that's poorly formatted:

````python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers import OutputFixingParser

# Step 1: Create base parser
parser = PydanticOutputParser(pydantic_object=Performer)

# Step 2: Wrap with smart parser
smart_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

# Step 3: Parse and auto-fix malformed data
malformed = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump',], 'age': '65'}"
fixed_response = smart_parser.parse(malformed)  # LLM fixes format issues

print(fixed_response.name)  # "Tom Hanks"
print(fixed_response.film_names)  # ["Forrest Gump"]
````

## 3. **Retry Logic with Validation**

Implement retry mechanism for invalid LLM outputs:

````python
from pydantic import ValidationError
from typing import Optional

def get_validated_output(
    prompt: str, 
    schema: type[BaseModel], 
    max_retries: int = 3
) -> Optional[BaseModel]:
    """Get LLM output with validation and retries"""
    
    llm_with_structure = llm.with_structured_output(schema)
    
    for attempt in range(max_retries):
        try:
            response = llm_with_structure.invoke(prompt)
            # If we get here, Pydantic validation passed
            return response
            
        except ValidationError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                # Add error feedback to prompt
                prompt += f"\n\nPrevious attempt had errors: {e}. Please fix."
            else:
                print("Max retries reached")
                return None
    
    return None

# Usage
result = get_validated_output(
    "Generate filmography for Tom Hanks with age and rating",
    Performer,
    max_retries=3
)
````

## 4. **Custom Validation with Fallback**

Validate after receiving output and use smart parser as fallback:

````python
def validate_and_fix_output(
    llm_response: str,
    schema: type[BaseModel]
) -> BaseModel:
    """Validate output and fix if needed"""
    
    # Try direct parsing first
    parser = PydanticOutputParser(pydantic_object=schema)
    
    try:
        # Attempt basic parsing
        result = parser.parse(llm_response)
        print("✓ Direct parsing successful")
        return result
        
    except Exception as e:
        print(f"✗ Direct parsing failed: {e}")
        print("→ Using smart parser to fix...")
        
        # Fallback to smart parser
        smart_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        try:
            result = smart_parser.parse(llm_response)
            print("✓ Smart parser fixed the output")
            return result
        except Exception as e:
            print(f"✗ Smart parser also failed: {e}")
            raise

# Usage
response = validate_and_fix_output(
    "{'name': 'Invalid', 'films': []}",  # Missing required fields
    Performer
)
````

## 5. **Comprehensive Validation Pipeline**

Full production-ready validation system:

````python
from typing import Tuple, Optional
from pydantic import ValidationError

class ValidationResult:
    def __init__(self, success: bool, data: Optional[BaseModel], errors: list):
        self.success = success
        self.data = data
        self.errors = errors

def comprehensive_validation(
    prompt: str,
    schema: type[BaseModel],
    max_retries: int = 3,
    use_smart_parser: bool = True
) -> ValidationResult:
    """
    Complete validation pipeline:
    1. Get LLM structured output
    2. Validate with Pydantic
    3. Retry with feedback if validation fails
    4. Use smart parser as final fallback
    """
    
    llm_with_structure = llm.with_structured_output(schema)
    errors = []
    
    # Phase 1: Try with retries and feedback
    for attempt in range(max_retries):
        try:
            response = llm_with_structure.invoke(prompt)
            
            # Additional custom validation
            if hasattr(response, 'film_names') and not response.film_names:
                raise ValueError("Film list cannot be empty")
            
            return ValidationResult(success=True, data=response, errors=[])
            
        except (ValidationError, ValueError) as e:
            error_msg = f"Attempt {attempt + 1}: {str(e)}"
            errors.append(error_msg)
            print(error_msg)
            
            if attempt < max_retries - 1:
                # Add error context to next attempt
                prompt += f"\n\nError from previous attempt: {e}\nPlease correct these issues."
    
    # Phase 2: Smart parser fallback (if enabled)
    if use_smart_parser:
        print("\n→ All attempts failed. Trying smart parser...")
        try:
            # Get raw string output
            raw_response = llm.invoke(prompt).content
            
            # Use smart parser
            parser = PydanticOutputParser(pydantic_object=schema)
            smart_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
            fixed_data = smart_parser.parse(raw_response)
            
            print("✓ Smart parser succeeded!")
            return ValidationResult(success=True, data=fixed_data, errors=errors)
            
        except Exception as e:
            errors.append(f"Smart parser failed: {e}")
    
    return ValidationResult(success=False, data=None, errors=errors)

# Usage example
result = comprehensive_validation(
    "Generate filmography for Tom Hanks with age and rating",
    Performer,
    max_retries=3,
    use_smart_parser=True
)

if result.success:
    print(f"\n✓ Success! Got: {result.data.name}")
    print(f"Films: {result.data.film_names}")
else:
    print(f"\n✗ Failed after all attempts")
    print(f"Errors: {result.errors}")
````

## 6. **Validation with include_raw Parameter**

Get both structured output and raw response for debugging:

````python
llm_with_structure = llm.with_structured_output(
    Performer,
    include_raw=True  # Returns both parsed and raw
)

response = llm_with_structure.invoke("Generate filmography")

# response is now a dict with 'parsed' and 'raw'
structured_data = response['parsed']  # Pydantic object
raw_output = response['raw']  # Original LLM response

# Validate and fall back to smart parser if needed
if not structured_data or not structured_data.film_names:
    print("Validation failed, using smart parser...")
    parser = PydanticOutputParser(pydantic_object=Performer)
    smart_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    structured_data = smart_parser.parse(raw_output.content)
````

## Summary: Validation Strategy

1. **Prevention**: Use Pydantic validators to catch issues early
2. **Detection**: Wrap LLM calls in try-except to catch ValidationError
3. **Retry**: Give LLM feedback about errors and retry
4. **Repair**: Use OutputFixingParser to fix formatting issues
5. **Fallback**: Have default values or alternative strategies

The `OutputFixingParser` is your safety net for when everything else fails!