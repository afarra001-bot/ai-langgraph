# Other Model Types in LangChain

Beyond **Chat Models** and **Text Completion Models**, LangChain supports several other model types:

## 1. **Embedding Models**

Convert text into numerical vector representations for semantic search and similarity comparisons.

````python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    api_key=api_key,
    base_url=base_url
)

# Generate embeddings for text
vector = embeddings.embed_query("What is Python?")
print(len(vector))  # Vector dimension (e.g., 1536 for OpenAI)

# Embed multiple documents
vectors = embeddings.embed_documents([
    "Python is a programming language",
    "JavaScript is used for web development"
])
````

**Use Cases**: Vector databases, semantic search, document similarity, RAG systems

## 2. **Tool/Function Calling Models**

Models that can call external functions/tools during conversation.

````python
from langchain_openai import ChatOpenAI

llm_with_tools = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model="gpt-4o-mini"
).bind_tools([weather_tool, calculator_tool])

response = llm_with_tools.invoke("What's 25 * 4?")
# Model returns a tool call request instead of text
````

**Use Cases**: Agents, calculators, API calls, database queries

## 3. **Multimodal Models**

Process multiple input types (text, images, audio, video).

````python
from langchain_openai import ChatOpenAI

multimodal_llm = ChatOpenAI(model="gpt-4o")

response = multimodal_llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
    ])
])
````

**Use Cases**: Image analysis, OCR, video understanding, audio transcription

## 4. **Reranking Models**

Score and reorder search results based on relevance to a query.

````python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

compressor = CohereRerank(api_key="cohere_api_key")
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)
````

**Use Cases**: Improving RAG retrieval, search result ranking

## 5. **Vision Models** (Specialized)

Dedicated models for image understanding tasks.

````python
# Example with specialized vision API
from langchain_community.llms import Replicate

vision_model = Replicate(model="stability-ai/sdxl")
image = vision_model.generate("A sunset over mountains")
````

**Use Cases**: Image generation (DALL-E, Stable Diffusion), image captioning

## 6. **Audio/Speech Models**

Text-to-speech and speech-to-text models.

````python
# Text-to-Speech
from openai import OpenAI
client = OpenAI(api_key=api_key)

speech = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello, this is a test"
)

# Speech-to-Text (Whisper)
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
````

**Use Cases**: Voice assistants, transcription, accessibility

## 7. **Fine-tuned/Custom Models**

Your own trained models deployed on various platforms.

````python
from langchain_openai import ChatOpenAI

custom_model = ChatOpenAI(
    api_key=api_key,
    base_url="https://your-custom-endpoint.com",
    model="your-fine-tuned-model-id"
)
````

**Use Cases**: Domain-specific tasks, specialized behavior

## Summary Table

| Model Type | Input | Output | Primary Use |
|------------|-------|--------|-------------|
| Chat | Messages | Response message | Conversations |
| Text Completion | Text string | Continued text | Text generation |
| Embedding | Text | Vector | Semantic search |
| Tool Calling | Messages + tools | Tool calls | Agents, automation |
| Multimodal | Text + images/audio | Response | Vision, audio tasks |
| Reranking | Query + documents | Ranked docs | Search improvement |

**In your notebook**, you're using a **Chat Model** (gpt-4o-mini), which is the most versatile for conversational AI applications.