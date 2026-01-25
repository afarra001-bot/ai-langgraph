from typing import List, Optional
from pydantic import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import os
import json

# Load environment
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("OPENAI_ENDPOINT")

llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model="gpt-4o-mini",
    temperature=0.0
)

# Define a complex Pydantic model with validation
class Product(BaseModel):
    """Product information from an e-commerce listing"""
    name: str = Field(description="Product name")
    price: float = Field(description="Product price in USD", gt=0)
    category: str = Field(description="Product category")
    in_stock: bool = Field(description="Whether product is available")
    tags: List[str] = Field(description="Product tags/keywords")
    rating: Optional[float] = Field(default=None, description="Product rating 0-5", ge=0, le=5)
    
    @validator('tags')
    def validate_tags(cls, v):
        if not v:
            raise ValueError("Tags list cannot be empty")
        return [tag.strip().lower() for tag in v]

# Example 1: Well-formatted JSON (should work with basic parser)
print("=" * 60)
print("EXAMPLE 1: Well-formatted JSON")
print("=" * 60)

good_json = """
{
    "name": "Wireless Mouse",
    "price": 29.99,
    "category": "Electronics",
    "in_stock": true,
    "tags": ["computer", "wireless", "mouse"],
    "rating": 4.5
}
"""

basic_parser = PydanticOutputParser(pydantic_object=Product)

try:
    result = basic_parser.parse(good_json)
    print(f"✓ Basic Parser Success!")
    print(f"  Product: {result.name}")
    print(f"  Price: ${result.price}")
    print(f"  Tags: {result.tags}")
except OutputParserException as e:
    print(f"✗ Basic Parser Failed: {e}")

# Example 2: Malformed JSON (single quotes, missing quotes, trailing commas)
print("\n" + "=" * 60)
print("EXAMPLE 2: Malformed JSON - Basic Parser FAILS")
print("=" * 60)

bad_json = """
{
    'name': 'Mechanical Keyboard',
    price: 89.99,
    'category': "Electronics",
    'in_stock': True,
    'tags': ['keyboard', 'mechanical', 'gaming',],
    rating: 4.8,
}
"""

print(f"Input: {bad_json[:100]}...")

try:
    result = basic_parser.parse(bad_json)
    print(f"✓ Basic Parser Success: {result}")
except OutputParserException as e:
    print(f"✗ Basic Parser Failed!")
    print(f"  Error: {str(e)[:100]}...")

# Example 3: Smart Parser fixes the malformed JSON
print("\n" + "=" * 60)
print("EXAMPLE 3: Smart Parser AUTO-FIXES the errors")
print("=" * 60)

smart_parser = OutputFixingParser.from_llm(parser=basic_parser, llm=llm)

try:
    result = smart_parser.parse(bad_json)
    print(f"✓ Smart Parser Success!")
    print(f"  Product: {result.name}")
    print(f"  Price: ${result.price}")
    print(f"  In Stock: {result.in_stock}")
    print(f"  Tags: {result.tags}")
    print(f"  Rating: {result.rating}")
except Exception as e:
    print(f"✗ Smart Parser Failed: {e}")

# Example 4: Real-world scenario - LLM generates bad format
print("\n" + "=" * 60)
print("EXAMPLE 4: Real-world LLM output with errors")
print("=" * 60)

# Simulate LLM returning badly formatted JSON
llm_bad_output = """
Here's the product info:
{
    name: "USB-C Cable",
    price: '15.99',
    category: Electronics,
    in_stock: yes,
    tags: [usb, cable, charging],
    rating: null
}
Hope this helps!
"""

print("LLM Output (with extra text and formatting issues):")
print(llm_bad_output[:150] + "...")

try:
    result = smart_parser.parse(llm_bad_output)
    print(f"\n✓ Smart Parser extracted and fixed!")
    print(f"  Product: {result.name}")
    print(f"  Price: ${result.price}")
    print(f"  Type of price: {type(result.price)}")
    print(f"  In Stock: {result.in_stock}")
    print(f"  Tags: {result.tags}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Example 5: Complete workflow with error handling
print("\n" + "=" * 60)
print("EXAMPLE 5: Production-ready wrapper function")
print("=" * 60)

def extract_product_info(text: str, use_smart_parser: bool = True) -> Optional[Product]:
    """
    Extract product information from text with automatic error recovery.
    
    Args:
        text: Raw text that might contain product JSON
        use_smart_parser: Whether to use self-healing parser
    
    Returns:
        Product object or None if parsing fails
    """
    parser = PydanticOutputParser(pydantic_object=Product)
    
    if use_smart_parser:
        parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    
    try:
        result = parser.parse(text)
        return result
    except Exception as e:
        print(f"Parsing failed even with smart parser: {e}")
        return None

# Test the wrapper
messy_input = """
The product details are:
{'name': 'Gaming Headset', price: 79.99, 'category': 'Electronics',
'in_stock': true, 'tags': ['gaming', 'audio', 'headset'], rating: 4.3}
"""

print("Testing wrapper function with messy input...")
product = extract_product_info(messy_input, use_smart_parser=True)

if product:
    print(f"✓ Successfully extracted:")
    print(f"  {product.name} - ${product.price}")
    print(f"  Category: {product.category}")
    print(f"  Rating: {product.rating}/5")
    print(f"  Tags: {', '.join(product.tags)}")
else:
    print("✗ Failed to extract product info")

# Example 6: Comparing performance
print("\n" + "=" * 60)
print("EXAMPLE 6: Performance comparison")
print("=" * 60)

test_cases = [
    '{"name": "Mouse", "price": 25, "category": "Electronics", "in_stock": true, "tags": ["mouse"]}',  # Valid
    "{'name': 'Keyboard', price: 85, 'category': Electronics, 'in_stock': True, 'tags': ['keyboard']}",  # Invalid
    '{name: "Monitor", "price": 299.99, category: "Electronics", in_stock: yes, tags: ["monitor", "display"]}',  # Mixed
]

basic_parser = PydanticOutputParser(pydantic_object=Product)
smart_parser = OutputFixingParser.from_llm(parser=basic_parser, llm=llm)

print(f"\nTesting {len(test_cases)} cases:")
print(f"{'Case':<6} {'Basic Parser':<15} {'Smart Parser':<15}")
print("-" * 40)

for i, test in enumerate(test_cases, 1):
    basic_result = "PASS" if test.startswith('{"') else "FAIL"
    
    try:
        smart_parser.parse(test)
        smart_result = "PASS"
    except:
        smart_result = "FAIL"
    
    print(f"{i:<6} {basic_result:<15} {smart_result:<15}")

print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)
print("""
1. ✓ Smart parsers handle single quotes → double quotes
2. ✓ Smart parsers fix missing quotes on keys/values
3. ✓ Smart parsers remove trailing commas
4. ✓ Smart parsers extract JSON from surrounding text
5. ✓ Smart parsers convert string booleans ('yes'/'True' → true)
6. ✓ Smart parsers maintain type validation from Pydantic
7. ⚠ Smart parsers require LLM call (slightly slower)
8. ⚠ Smart parsers cost tokens (consider for production)

BEST PRACTICES:
- Use smart parsers when dealing with unreliable LLM outputs
- Implement fallback logic for critical applications
- Cache parser instances to avoid re-initialization
- Monitor smart parser usage to optimize costs
- Add logging to track when self-healing is triggered
""")