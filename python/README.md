# 🐍 Albert API Python Client

A comprehensive Python client for interacting with the Albert API, based on the OpenAPI 3.1.0 specification.

## 📦 Installation

1. Install dependencies:

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install -e .
```

2. Set up environment variables:
```bash
export ALBERT_API_BASE_URL="https://albert.api.etalab.gouv.fr"
export ALBERT_API_KEY="your-api-key-here"
```
Or copy `.env.example` to `.env` and fill in your values.

## ⚡ Quick Start

**Run the test:**
```bash
uv run test.py
```

**Or use in your own code:**
```python
from albert_api import AlbertAPI

# Initialize the client
api = AlbertAPI()

# Get available models
models = api.get_models()
print(f"Available models: {len(models['data'])}")

# Simple chat completion
messages = [{"role": "user", "content": "Hello!"}]
response = api.chat_completions(
    messages=messages,
    model="albert-small",
    max_completion_tokens=100
)

print(response['choices'][0]['message']['content'])
```

## 💡 Usage Examples

### Chat Completions

```python
from albert_api import AlbertAPI

api = AlbertAPI()

# Basic chat completion
messages = [
    {"role": "user", "content": "Explain quantum computing in simple terms"}
]

response = api.chat_completions(
    messages=messages,
    model="albert-small",
    temperature=0.7,
    max_completion_tokens=200
)

# Streaming chat completion
response = api.chat_completions(
    messages=messages,
    model="albert-small",
    stream=True
)
```

### Embeddings

```python
# Create embeddings for text
texts = ["Hello world", "Bonjour le monde"]
embeddings = api.create_embeddings(
    input_text=texts,
    model="text-embedding-ada-002"
)

print(f"Embedding dimensions: {len(embeddings['data'][0]['embedding'])}")
```

### Document Processing

```python
# Parse a PDF document
parsed_doc = api.parse_document(
    file_path="document.pdf",
    output_format="markdown",
    force_ocr=False
)

# Extract text using OCR
ocr_result = api.ocr_document(
    file_path="scanned.pdf",
    model="ocr-model",
    dpi=150
)
```

### Collections and Search

```python
# Create a collection
collection = api.create_collection(
    name="My Documents",
    description="Personal document collection",
    visibility="private"
)

# Upload a document to the collection
document = api.create_document(
    file_path="document.pdf",
    collection_id=collection['id'],
    chunk_size=2048
)

# Search across collections
search_results = api.search(
    prompt="What is machine learning?",
    collections=[collection['id']],
    k=5,
    method="semantic"
)
```

### Audio Transcription

```python
# Transcribe audio file
transcription = api.transcribe_audio(
    file_path="audio.mp3",
    model="whisper-1",
    language="fr",
    response_format="json"
)

print(f"Transcription: {transcription['text']}")
```

### Usage Tracking

```python
# Get usage information
usage = api.get_usage(
    limit=50,
    page=1,
    order_by="datetime",
    order_direction="desc"
)

print(f"Total requests: {usage['total_requests']}")
print(f"Total tokens: {usage['total_tokens']}")
print(f"Total CO2: {usage['total_co2']} grams")
```

## 📚 API Reference

### Core Methods

#### Models
- `get_models()` - List available models
- `get_model(model_id)` - Get specific model information

#### Chat Completions
- `chat_completions(messages, model, **kwargs)` - Create chat completion
- `agents_completions(messages, model, **kwargs)` - Create agent completion with tools
- `get_agents_tools()` - Get available agent tools

#### Embeddings
- `create_embeddings(input_text, model, **kwargs)` - Create text embeddings

#### Document Processing
- `parse_document(file_path, **kwargs)` - Parse document
- `ocr_document(file_path, model, **kwargs)` - Extract text with OCR

#### Collections & Documents
- `create_collection(name, description, visibility)` - Create collection
- `get_collections(offset, limit)` - List collections
- `create_document(file_path, collection_id, **kwargs)` - Upload document
- `get_documents(collection_id, limit, offset)` - List documents

#### Search & RAG
- `search(prompt, collections, **kwargs)` - Search documents
- `rerank(prompt, input_texts, model)` - Rerank texts by relevance

#### Audio
- `transcribe_audio(file_path, model, **kwargs)` - Transcribe audio

#### Usage & Tokens
- `get_usage(limit, page, **kwargs)` - Get usage statistics
- `create_token(name, user, expires_at)` - Create API token
- `get_tokens(offset, limit, **kwargs)` - List tokens

## ⚙️ Configuration

The client can be configured using environment variables or constructor parameters:

```python
# Using environment variables (recommended)
api = AlbertAPI()

# Using constructor parameters
api = AlbertAPI(
    base_url="https://api.albert.numerique.gouv.fr",
    api_key="your-api-key",
    timeout=30
)
```

## ⚠️ Error Handling

The client raises `RuntimeError` for API-related errors:

```python
from albert_api import AlbertAPI

try:
    api = AlbertAPI()
    response = api.chat_completions(messages, model)
except RuntimeError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔄 Context Manager

The client supports context manager usage for automatic cleanup:

```python
from albert_api import AlbertAPI

with AlbertAPI() as api:
    response = api.chat_completions(messages, model)
    # Session automatically closed when exiting context
```

## 🛠️ Code Quality

Lint and format the code with Ruff:

```bash
ruff check --fix . && ruff format .
```

## 🔧 Environment Variables

The client uses environment variables from the system environment. For testing, the demo script automatically loads environment variables from a `.env` file if present.

| Variable | Description | Default |
|----------|-------------|---------|
| `ALBERT_API_BASE_URL` | Base URL for the Albert API | Required |
| `ALBERT_API_KEY` | Your API key for authentication | Required |

### Setting environment variables:

**For testing (recommended):**
Create a `.env` file in the project root:
```env
ALBERT_API_BASE_URL=https://albert.api.etalab.gouv.fr
ALBERT_API_KEY=your-api-key-here
```

**In your shell:**
```bash
export ALBERT_API_BASE_URL=https://albert.api.etalab.gouv.fr
export ALBERT_API_KEY=your-api-key-here
```
