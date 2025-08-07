#!/usr/bin/env node
/**
 * Albert API TypeScript Test Script
 * 
 * A test script for the Albert API TypeScript client.
 * 
 * Documentation:
 * - API Documentation: https://albert.api.etalab.gouv.fr/documentation
 * - Swagger UI: https://albert.api.etalab.gouv.fr/swagger
 * 
 * Usage:
 * - Run initialization test: npm run test
 * - Run models test: npm run test:models
 * - Run chat completions test: npm run test:completions
 * - Run embeddings test: npm run test:embeddings
 * - Run usage test: npm run test:usage
 * - Run collections test: npm run test:collections
 * - Run documents test: npm run test:documents
 * - Run search test: npm run test:search
 * - Run all tests: npm run test:all
 */

import { AlbertAPI } from './albert-api'

async function test_initialization(): Promise<void> {
  console.log("🚀 Albert API TypeScript Playground - Initialization Test")
  console.log("=".repeat(60))

  // Check if API key is available
  if (!process.env.ALBERT_API_KEY) {
    console.log("❌ ALBERT_API_KEY environment variable is not set!")
    console.log("Please set it with: export ALBERT_API_KEY='your-api-key'")
    console.log("\nExample usage:")
    console.log("  export ALBERT_API_KEY='your-api-key-here'")
    console.log("  npm run test")
    return
  }

  try {
    // Initialize the API client
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Test basic connectivity
    console.log("\n🔍 Testing basic connectivity...")
    const models = await api.get_models()
    console.log(`✅ Successfully connected! Found ${models.data?.length || 0} models`)

    api.close()
    console.log("\n✅ Initialization test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Initialization Error: ${error.message}`)
  }
}

async function test_models(): Promise<void> {
  console.log("🧪 Testing Models Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get all models
    console.log("\n📋 Getting all available models:")
    const models = await api.get_models()
    
    if (models.data && models.data.length > 0) {
      models.data.forEach((model: any, index: number) => {
        console.log(`  ${index + 1}. ${model.id} (${model.type})`)
        console.log(`     - Created: ${new Date(model.created * 1000).toISOString()}`)
        console.log(`     - Owned by: ${model.owned_by}`)
        if (model.max_context_length) {
          console.log(`     - Max context length: ${model.max_context_length}`)
        }
        console.log("")
      })
    } else {
      console.log("ℹ️  No models found")
    }

    // Test getting a specific model
    if (models.data && models.data.length > 0) {
      const firstModel = models.data[0]
      console.log(`🔍 Testing get_model for: ${firstModel.id}`)
      const modelDetails = await api.get_model(firstModel.id)
      console.log(`✅ Successfully retrieved details for ${modelDetails.id}`)
    }

    api.close()
    console.log("\n✅ Models test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Models Test Error: ${error.message}`)
  }
}

async function test_completions(): Promise<void> {
  console.log("🧪 Testing Chat Completions Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get text-generation models
    const models = await api.get_models()
    const textModels = models.data?.filter((m: any) => m.type === 'text-generation') || []
    
    if (textModels.length === 0) {
      console.log("ℹ️  No text-generation models available")
      return
    }

    const model = textModels[0].id
    console.log(`🎯 Using model: ${model}`)

    // Test 1: Simple completion
    console.log("\n📝 Test 1: Simple completion")
    const response1 = await api.chat_completions(
      [{ role: 'user', content: 'Explain quantum computing in one sentence.' }],
      model,
      { max_completion_tokens: 100 }
    )
    
    if (response1.choices && response1.choices[0]?.message?.content) {
      console.log(`🤖 Response: ${response1.choices[0].message.content}`)
      console.log(`📊 Tokens used: ${response1.usage?.total_tokens || 0}`)
    } else {
      console.log("❌ No response received")
    }

    // Test 2: French conversation
    console.log("\n🇫🇷 Test 2: French conversation")
    const response2 = await api.chat_completions(
      [
        { role: 'system', content: 'Tu es un assistant français très utile.' },
        { role: 'user', content: 'Qu\'est-ce que l\'intelligence artificielle ?' }
      ],
      model,
      { max_completion_tokens: 150 }
    )
    
    if (response2.choices && response2.choices[0]?.message?.content) {
      console.log(`🤖 Response: ${response2.choices[0].message.content}`)
    } else {
      console.log("❌ No response received")
    }

    // Test 3: Code generation
    console.log("\n💻 Test 3: Code generation")
    const response3 = await api.chat_completions(
      [{ role: 'user', content: 'Write a TypeScript function to calculate factorial.' }],
      model,
      { max_completion_tokens: 200 }
    )
    
    if (response3.choices && response3.choices[0]?.message?.content) {
      console.log(`🤖 Response: ${response3.choices[0].message.content}`)
    } else {
      console.log("❌ No response received")
    }

    api.close()
    console.log("\n✅ Chat completions test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Completions Test Error: ${error.message}`)
  }
}

async function test_embeddings(): Promise<void> {
  console.log("🧪 Testing Embeddings Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get embedding models
    const models = await api.get_models()
    const embeddingModels = models.data?.filter((m: any) => m.type === 'text-embeddings-inference') || []
    
    if (embeddingModels.length === 0) {
      console.log("ℹ️  No embedding models available")
      return
    }

    const model = embeddingModels[0].id
    console.log(`🎯 Using model: ${model}`)

    // Test single text embedding
    console.log("\n📝 Test 1: Single text embedding")
    const text1 = "Hello, this is a test sentence for embeddings."
    const response1 = await api.create_embeddings(text1, model)
    
    if (response1.data && response1.data[0]?.embedding) {
      console.log(`✅ Successfully created embedding with ${response1.data[0].embedding.length} dimensions`)
      console.log(`📊 Tokens used: ${response1.usage?.total_tokens || 0}`)
    } else {
      console.log("❌ No embedding received")
    }

    // Test multiple texts embedding
    console.log("\n📝 Test 2: Multiple texts embedding")
    const texts = [
      "First sentence for embedding.",
      "Second sentence for embedding.",
      "Third sentence for embedding."
    ]
    const response2 = await api.create_embeddings(texts, model)
    
    if (response2.data && response2.data.length > 0) {
      console.log(`✅ Successfully created ${response2.data.length} embeddings`)
      response2.data.forEach((item: any, index: number) => {
        console.log(`  ${index + 1}. ${texts[index]} → ${item.embedding.length} dimensions`)
      })
    } else {
      console.log("❌ No embeddings received")
    }

    api.close()
    console.log("\n✅ Embeddings test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Embeddings Test Error: ${error.message}`)
  }
}

async function test_usage(): Promise<void> {
  console.log("🧪 Testing Usage Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get usage information
    console.log("\n📊 Getting usage information:")
    const usage = await api.get_usage(5, 1) // Get first 5 records
    
    console.log(`  Total requests: ${usage.total_requests || 0}`)
    console.log(`  Total tokens: ${usage.total_tokens || 0}`)
    console.log(`  Total CO2: ${usage.total_co2 || 0} grams`)
    console.log(`  Total pages: ${usage.total_pages || 0}`)
    console.log(`  Current page: ${usage.page || 0}`)
    console.log(`  Records per page: ${usage.limit || 0}`)

    if (usage.data && usage.data.length > 0) {
      console.log("\n📋 Recent usage records:")
      usage.data.slice(0, 3).forEach((record: any, index: number) => {
        console.log(`  ${index + 1}. ${new Date(record.datetime * 1000).toISOString()}`)
        console.log(`     - Endpoint: ${record.endpoint}`)
        console.log(`     - Model: ${record.model || 'N/A'}`)
        console.log(`     - Tokens: ${record.total_tokens || 0}`)
        console.log(`     - Cost: ${record.cost || 0}`)
        console.log("")
      })
    } else {
      console.log("ℹ️  No usage records found")
    }

    api.close()
    console.log("\n✅ Usage test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Usage Test Error: ${error.message}`)
  }
}

async function test_collections(): Promise<void> {
  console.log("🧪 Testing Collections Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get existing collections
    console.log("\n📋 Getting existing collections:")
    const collections = await api.get_collections()
    
    if (collections.data && collections.data.length > 0) {
      collections.data.forEach((collection: any, index: number) => {
        console.log(`  ${index + 1}. ${collection.name} (ID: ${collection.id})`)
        console.log(`     - Description: ${collection.description || 'No description'}`)
        console.log(`     - Visibility: ${collection.visibility}`)
        console.log(`     - Documents: ${collection.documents}`)
        console.log(`     - Created: ${new Date(collection.created_at * 1000).toISOString()}`)
        console.log("")
      })
    } else {
      console.log("ℹ️  No collections found")
    }

    // Test creating a new collection
    console.log("📝 Test: Creating a new test collection")
    const testCollectionName = `test-collection-${Date.now()}`
    const newCollection = await api.create_collection(
      testCollectionName,
      "Test collection created by TypeScript client",
      "private"
    )
    
    if (newCollection.id) {
      console.log(`✅ Successfully created collection: ${testCollectionName} (ID: ${newCollection.id})`)
      
      // Test getting the specific collection
      console.log("🔍 Test: Getting specific collection")
      const retrievedCollection = await api.get_collection(newCollection.id)
      console.log(`✅ Retrieved collection: ${retrievedCollection.name}`)
      
      // Test updating the collection
      console.log("✏️  Test: Updating collection")
      await api.update_collection(newCollection.id, {
        description: "Updated test collection description"
      })
      console.log("✅ Successfully updated collection")
      
      // Test deleting the collection
      console.log("🗑️  Test: Deleting collection")
      await api.delete_collection(newCollection.id)
      console.log("✅ Successfully deleted collection")
    } else {
      console.log("❌ Failed to create collection")
    }

    api.close()
    console.log("\n✅ Collections test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Collections Test Error: ${error.message}`)
  }
}

async function test_documents(): Promise<void> {
  console.log("🧪 Testing Documents Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get existing documents
    console.log("\n📋 Getting existing documents:")
    const documents = await api.get_documents()
    
    if (documents.data && documents.data.length > 0) {
      documents.data.forEach((document: any, index: number) => {
        console.log(`  ${index + 1}. ${document.name} (ID: ${document.id})`)
        console.log(`     - Collection ID: ${document.collection_id}`)
        console.log(`     - Chunks: ${document.chunks || 0}`)
        console.log(`     - Created: ${new Date(document.created_at * 1000).toISOString()}`)
        console.log("")
      })
    } else {
      console.log("ℹ️  No documents found")
    }

    // Test getting a specific document if available
    if (documents.data && documents.data.length > 0) {
      const firstDoc = documents.data[0]
      console.log(`🔍 Test: Getting specific document (ID: ${firstDoc.id})`)
      const documentDetails = await api.get_document(firstDoc.id)
      console.log(`✅ Retrieved document: ${documentDetails.name}`)
      
      // Test getting chunks for this document
      console.log("📄 Test: Getting document chunks")
      const chunks = await api.get_chunks(firstDoc.id, 3) // Get first 3 chunks
      
      if (chunks.data && chunks.data.length > 0) {
        console.log(`✅ Found ${chunks.data.length} chunks`)
        chunks.data.forEach((chunk: any, index: number) => {
          console.log(`  Chunk ${chunk.id}: ${chunk.content.substring(0, 100)}...`)
        })
      } else {
        console.log("ℹ️  No chunks found for this document")
      }
    }

    api.close()
    console.log("\n✅ Documents test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Documents Test Error: ${error.message}`)
  }
}

async function test_search(): Promise<void> {
  console.log("🧪 Testing Search Endpoint")
  console.log("=".repeat(50))

  try {
    const api = new AlbertAPI()
    console.log("✅ Albert API client initialized successfully!")

    // Get collections for search
    console.log("\n🔍 Getting collections for search:")
    const collections = await api.get_collections()
    
    if (collections.data && collections.data.length > 0) {
      const collectionIds = collections.data.map((c: any) => c.id)
      console.log(`Found ${collectionIds.length} collections: ${collectionIds.join(', ')}`)
      
      // Test search
      console.log("\n🔍 Test: Searching in collections")
      const searchQuery = "artificial intelligence"
      const searchResults = await api.search(searchQuery, collectionIds, {
        k: 3,
        method: "semantic"
      })
      
      if (searchResults.data && searchResults.data.length > 0) {
        console.log(`✅ Found ${searchResults.data.length} search results for "${searchQuery}":`)
        searchResults.data.forEach((result: any, index: number) => {
          console.log(`  ${index + 1}. Score: ${result.score.toFixed(3)}`)
          console.log(`     - Method: ${result.method}`)
          console.log(`     - Content: ${result.chunk.content.substring(0, 150)}...`)
          console.log("")
        })
      } else {
        console.log("ℹ️  No search results found")
      }
    } else {
      console.log("ℹ️  No collections available for search")
    }

    api.close()
    console.log("\n✅ Search test completed successfully!")

  } catch (error: any) {
    console.error(`❌ Search Test Error: ${error.message}`)
  }
}

async function test_all(): Promise<void> {
  console.log("🧪 Running All Tests")
  console.log("=".repeat(50))

  const tests = [
    { name: "Initialization", fn: test_initialization },
    { name: "Models", fn: test_models },
    { name: "Completions", fn: test_completions },
    { name: "Embeddings", fn: test_embeddings },
    { name: "Usage", fn: test_usage },
    { name: "Collections", fn: test_collections },
    { name: "Documents", fn: test_documents },
    { name: "Search", fn: test_search }
  ]

  for (const test of tests) {
    console.log(`\n🚀 Running ${test.name} Test...`)
    console.log("-".repeat(30))
    await test.fn()
    console.log(`✅ ${test.name} Test Completed`)
  }

  console.log("\n🎉 All tests completed!")
}

// Command line argument handling
const args = process.argv.slice(2)

if (args.includes('--models')) {
  test_models()
} else if (args.includes('--completions')) {
  test_completions()
} else if (args.includes('--embeddings')) {
  test_embeddings()
} else if (args.includes('--usage')) {
  test_usage()
} else if (args.includes('--collections')) {
  test_collections()
} else if (args.includes('--documents')) {
  test_documents()
} else if (args.includes('--search')) {
  test_search()
} else if (args.includes('--all')) {
  test_all()
} else {
  // Default: run initialization test
  test_initialization()
} 
