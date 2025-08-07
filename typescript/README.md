# 🔷 Albert API TypeScript Client

A comprehensive TypeScript client for interacting with the Albert API, based on the OpenAPI 3.1.0 specification.

## 📦 Installation

```bash
npm install
```

## 🔨 Build

```bash
npm run build
```

## 🚀 Development

```bash
npm run dev
```

## ⚡ Quick Start

### Basic Usage

```typescript
import { AlbertAPI } from './dist'

// Initialize with environment variables
const api = new AlbertAPI()

// Or initialize with custom configuration
const api = new AlbertAPI(
  'https://albert.api.etalab.gouv.fr',
  'your-api-key-here',
  30 // timeout in seconds
)
```

### Chat Completions

```typescript
const response = await api.chat_completions(
  [
    { role: 'user', content: 'Hello, how are you?' }
  ],
  'albert-small',
  {
    max_completion_tokens: 100,
    temperature: 0.7
  }
)

console.log(response.choices[0].message.content)
```

### Embeddings

```typescript
const embeddings = await api.create_embeddings(
  'Hello, this is a test sentence.',
  'embeddings-small'
)

console.log(`Embedding dimensions: ${embeddings.data[0].embedding.length}`)
```

### Collections Management

```typescript
// Create a collection
const collection = await api.create_collection(
  'my-collection',
  'Description of my collection',
  'private'
)

// List collections
const collections = await api.get_collections()

// Search in collections
const results = await api.search(
  'artificial intelligence',
  [collection.id],
  { k: 5, method: 'semantic' }
)
```

## 🧪 Testing

The project includes comprehensive test suites for each Albert API endpoint. Each test can be run individually or all together.

### Run initialization test (default):
```bash
npm run test
```

### Run specific endpoint tests:
```bash
npm run test:models          # Test models endpoint
npm run test:completions     # Test chat completions
npm run test:embeddings      # Test embeddings
npm run test:usage           # Test usage tracking
npm run test:collections     # Test collections management
npm run test:documents       # Test documents and chunks
npm run test:search          # Test search functionality
```

### Run all tests:
```bash
npm run test:all
```

### Run with custom environment:
```bash
ALBERT_API_KEY=your-key npm run test
```

## 📚 API Reference

### Core Methods

#### `constructor(base_url?, api_key?, timeout?)`
Initialize the Albert API client.

- `base_url` (optional): Base URL for the API (defaults to `ALBERT_API_BASE_URL` env var)
- `api_key` (optional): API key for authentication (defaults to `ALBERT_API_KEY` env var)
- `timeout` (optional): Request timeout in seconds (default: 30)

#### `close()`
Close the client and clean up resources.

### Models

#### `get_models()`
Get list of all available models.

#### `get_model(model: string)`
Get information about a specific model.

#### `get_models_ids(): Promise<string[]>`
Get list of model IDs.

### Chat Completions

#### `chat_completions(messages, model, kwargs?)`
Create a chat completion.

- `messages`: Array of message objects with `role` and `content`
- `model`: Model name/ID to use
- `kwargs`: Additional parameters (temperature, max_tokens, etc.)

#### `agents_completions(messages, model, kwargs?)`
Create an agent completion with MCP bridge tools.

#### `get_agents_tools()`
Get available tools for agents.

### Embeddings

#### `create_embeddings(input, model, kwargs?)`
Create embeddings for text.

- `input`: String or array of strings to embed
- `model`: Embedding model to use
- `kwargs`: Additional parameters

### Audio Transcription

#### `transcribe_audio(file_path, model, kwargs?)`
Transcribe audio file to text.

- `file_path`: Path to audio file (mp3, wav)
- `model`: Transcription model to use
- `kwargs`: Additional parameters (language, response_format, etc.)

### Document Processing

#### `parse_document(file_path, kwargs?)`
Parse a document (PDF, etc.).

#### `ocr_document(file_path, model, kwargs?)`
Extract text from PDF using OCR.

### Collections Management

#### `create_collection(name, description?, visibility?)`
Create a new collection.

#### `get_collections(offset?, limit?)`
Get list of collections.

#### `get_collection(collection_id)`
Get collection by ID.

#### `update_collection(collection_id, kwargs)`
Update collection properties.

#### `delete_collection(collection_id)`
Delete a collection.

### Documents

#### `create_document(file_path, collection_id, kwargs?)`
Create a document in a collection.

#### `get_documents(collection_id?, limit?, offset?)`
Get documents from collection.

#### `get_document(document_id)`
Get document by ID.

#### `delete_document(document_id)`
Delete a document.

### Chunks

#### `get_chunks(document_id, limit?, offset?)`
Get chunks of a document.

#### `get_chunk(document_id, chunk_id)`
Get specific chunk of a document.

### Search

#### `search(prompt, collections?, kwargs?)`
Search for relevant chunks.

- `prompt`: Search query
- `collections`: Array of collection IDs to search in
- `kwargs`: Additional parameters (method, k, score_threshold, etc.)

### Rerank

#### `rerank(prompt, input_texts, model)`
Rerank texts by relevance to prompt.

### Usage

#### `get_usage(limit?, page?, kwargs?)`
Get account usage information.

### Token Management

#### `create_token(name, user?, expires_at?)`
Create a new token.

#### `get_tokens(offset?, limit?, kwargs?)`
Get list of tokens.

#### `get_token(token_id)`
Get token by ID.

#### `delete_token(token_id)`
Delete a token.

## 🔧 Environment Variables

The client uses environment variables from the system environment. For testing, the test script automatically loads environment variables from a `.env` file if present.

- `ALBERT_API_BASE_URL`: Base URL for the Albert API (default: `https://albert.api.etalab.gouv.fr`)
- `ALBERT_API_KEY`: API key for authentication (required)

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

**Or when running commands:**
```bash
ALBERT_API_KEY=your-key npm run test
```

## ⚠️ Error Handling

The client throws descriptive errors for various failure scenarios:

- **Missing API Key**: "API key is required. Set ALBERT_API_KEY environment variable or pass api_key parameter."
- **Missing Base URL**: "Base URL is required. Set ALBERT_API_BASE_URL environment variable or pass base_url parameter."
- **API Errors**: Detailed error messages from the Albert API
- **Network Errors**: Connection and timeout errors

## 💡 Examples

### Complete Example

```typescript
import { AlbertAPI } from './dist'

async function main() {
  try {
    const api = new AlbertAPI()
    
    // Get available models
    const models = await api.get_models()
    console.log(`Available models: ${models.data.length}`)
    
    // Create a chat completion
    const response = await api.chat_completions(
      [{ role: 'user', content: 'Explain quantum computing' }],
      'albert-small',
      { max_completion_tokens: 100 }
    )
    
    console.log(response.choices[0].message.content)
    
    // Get usage information
    const usage = await api.get_usage()
    console.log(`Total tokens used: ${usage.total_tokens}`)
    
    api.close()
  } catch (error) {
    console.error('Error:', error.message)
  }
}

main()
```

### Working with Collections

```typescript
// Create a collection
const collection = await api.create_collection(
  'my-documents',
  'Collection for my documents',
  'private'
)

// Upload a document
const document = await api.create_document(
  './my-document.pdf',
  collection.id,
  { chunk_size: 2048 }
)

// Search in the collection
const results = await api.search(
  'artificial intelligence',
  [collection.id],
  { k: 5 }
)

console.log(`Found ${results.data.length} relevant chunks`)
```
