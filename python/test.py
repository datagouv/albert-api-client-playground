#!/usr/bin/env python3
"""
Albert API Python Client - Testing and Demo

This script demonstrates how to use the AlbertAPI client.
Run this to test the API functionality.

Usage:
    python test.py                    # Run initialization test (default)
    python test.py --models           # Test models endpoint
    python test.py --completions      # Test chat completions
    python test.py --embeddings       # Test embeddings
    python test.py --usage            # Test usage tracking
    python test.py --collections      # Test collections management
    python test.py --documents        # Test documents and chunks
    python test.py --search           # Test search functionality
    python test.py --all              # Run all tests
"""

import os
import sys
import time
from dotenv import load_dotenv
from albert_api import AlbertAPI

# Load environment variables from .env file for testing
load_dotenv()


def test_initialization() -> None:
    """Test client initialization and basic connectivity."""
    print("🚀 Albert API Python Playground - Initialization Test")
    print("=" * 60)

    # Check if API key is available
    if not os.getenv("ALBERT_API_KEY"):
        print("❌ ALBERT_API_KEY environment variable is not set!")
        print("Please set it with: export ALBERT_API_KEY='your-api-key'")
        print("\nExample usage:")
        print("  export ALBERT_API_KEY='your-api-key-here'")
        print("  python test.py")
        return

    try:
        # Initialize the API client
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Test basic connectivity
        print("\n🔍 Testing basic connectivity...")
        models = api.get_models()
        print(f"✅ Successfully connected! Found {len(models.get('data', []))} models")

        api.close()
        print("\n✅ Initialization test completed successfully!")

    except Exception as e:
        print(f"❌ Initialization Error: {e}")


def test_models() -> None:
    """Test models endpoint."""
    print("🧪 Testing Models Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get all models
        print("\n📋 Getting all available models:")
        models = api.get_models()

        if models.get("data"):
            indent = "     "
            for i, model in enumerate(models["data"], 1):
                mid = model["id"]
                aliases = model.get("aliases") or []
                aka = f" (aliases: {', '.join(aliases)})" if aliases else ""
                print(f"  {i}. {mid}{aka}")
                print(f"{indent}Type: {model.get('type', 'N/A')}")
                print(f"{indent}Created: {model.get('created', 'N/A')}")
                print(f"{indent}Owned by: {model.get('owned_by', 'N/A')}")
                if model.get("max_context_length"):
                    print(f"{indent}Max context length: {model['max_context_length']}")
                print()

        # Test getting a specific model
        if models.get("data"):
            first_model = models["data"][0]
            print(f"🔍 Testing get_model for: {first_model['id']}")
            model_details = api.get_model(first_model["id"])
            print(f"✅ Successfully retrieved details for {model_details['id']}")

        api.close()
        print("\n✅ Models test completed successfully!")

    except Exception as e:
        print(f"❌ Models Test Error: {e}")


def test_completions() -> None:
    """Test chat completions endpoint."""
    print("🧪 Testing Chat Completions Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get text-generation models
        models = api.get_models()
        text_models = [
            m for m in models.get("data", []) if m["type"] == "text-generation"
        ]

        if not text_models:
            print("ℹ️  No text-generation models available")
            return

        model = text_models[0]["id"]
        print(f"🎯 Using model: {model}")

        # Test 1: Simple completion
        print("\n📝 Test 1: Simple completion")
        response1 = api.chat_completions(
            [{"role": "user", "content": "Explain quantum computing in one sentence."}],
            model,
            max_completion_tokens=100,
        )

        if response1.get("choices") and response1["choices"][0].get("message", {}).get(
            "content"
        ):
            print(f"🤖 Response: {response1['choices'][0]['message']['content']}")
            print(
                f"📊 Tokens used: {response1.get('usage', {}).get('total_tokens', 0)}"
            )
        else:
            print("❌ No response received")

        # Test 2: French conversation
        print("\n🇫🇷 Test 2: French conversation")
        response2 = api.chat_completions(
            [
                {
                    "role": "system",
                    "content": "Tu es un assistant français très utile.",
                },
                {
                    "role": "user",
                    "content": "Qu'est-ce que l'intelligence artificielle ?",
                },
            ],
            model,
            max_completion_tokens=150,
        )

        if response2.get("choices") and response2["choices"][0].get("message", {}).get(
            "content"
        ):
            print(f"🤖 Response: {response2['choices'][0]['message']['content']}")
        else:
            print("❌ No response received")

        # Test 3: Code generation
        print("\n💻 Test 3: Code generation")
        response3 = api.chat_completions(
            [
                {
                    "role": "user",
                    "content": "Write a Python function to calculate factorial.",
                }
            ],
            model,
            max_completion_tokens=200,
        )

        if response3.get("choices") and response3["choices"][0].get("message", {}).get(
            "content"
        ):
            print(f"🤖 Response: {response3['choices'][0]['message']['content']}")
        else:
            print("❌ No response received")

        api.close()
        print("\n✅ Chat completions test completed successfully!")

    except Exception as e:
        print(f"❌ Completions Test Error: {e}")


def test_embeddings() -> None:
    """Test embeddings endpoint."""
    print("🧪 Testing Embeddings Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get embedding models
        models = api.get_models()
        embedding_models = [
            m
            for m in models.get("data", [])
            if m["type"] == "text-embeddings-inference"
        ]

        if not embedding_models:
            print("ℹ️  No embedding models available")
            return

        model = embedding_models[0]["id"]
        print(f"🎯 Using model: {model}")

        # Test single text embedding
        print("\n📝 Test 1: Single text embedding")
        text1 = "Hello, this is a test sentence for embeddings."
        response1 = api.create_embeddings(text1, model)

        if response1.get("data") and response1["data"][0].get("embedding"):
            print(
                f"✅ Successfully created embedding with {len(response1['data'][0]['embedding'])} dimensions"
            )
            print(
                f"📊 Tokens used: {response1.get('usage', {}).get('total_tokens', 0)}"
            )
        else:
            print("❌ No embedding received")

        # Test multiple texts embedding
        print("\n📝 Test 2: Multiple texts embedding")
        texts = [
            "First sentence for embedding.",
            "Second sentence for embedding.",
            "Third sentence for embedding.",
        ]
        response2 = api.create_embeddings(texts, model)

        if response2.get("data"):
            print(f"✅ Successfully created {len(response2['data'])} embeddings")
            for i, item in enumerate(response2["data"]):
                print(f"  {i + 1}. {texts[i]} → {len(item['embedding'])} dimensions")
        else:
            print("❌ No embeddings received")

        api.close()
        print("\n✅ Embeddings test completed successfully!")

    except Exception as e:
        print(f"❌ Embeddings Test Error: {e}")


def test_usage() -> None:
    """Test usage endpoint."""
    print("🧪 Testing Usage Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get usage information
        print("\n📊 Getting usage information:")
        usage = api.get_usage(limit=5, page=1)

        print(f"  Total requests: {usage.get('total_requests', 0)}")
        print(f"  Total tokens: {usage.get('total_tokens', 0)}")
        print(f"  Total CO2: {usage.get('total_co2', 0)} grams")
        print(f"  Total pages: {usage.get('total_pages', 0)}")
        print(f"  Current page: {usage.get('page', 0)}")
        print(f"  Records per page: {usage.get('limit', 0)}")

        if usage.get("data"):
            print("\n📋 Recent usage records:")
            for i, record in enumerate(usage["data"][:3], 1):
                print(f"  {i}. {record.get('datetime', 'N/A')}")
                print(f"     - Endpoint: {record.get('endpoint', 'N/A')}")
                print(f"     - Model: {record.get('model', 'N/A')}")
                print(f"     - Tokens: {record.get('total_tokens', 0)}")
                print(f"     - Cost: {record.get('cost', 0)}")
                print()
        else:
            print("ℹ️  No usage records found")

        api.close()
        print("\n✅ Usage test completed successfully!")

    except Exception as e:
        print(f"❌ Usage Test Error: {e}")


def test_collections() -> None:
    """Test collections endpoint."""
    print("🧪 Testing Collections Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get existing collections
        print("\n📋 Getting existing collections:")
        collections = api.get_collections()

        if collections.get("data"):
            for i, collection in enumerate(collections["data"], 1):
                print(f"  {i}. {collection['name']} (ID: {collection['id']})")
                print(
                    f"     - Description: {collection.get('description', 'No description')}"
                )
                print(f"     - Visibility: {collection.get('visibility', 'N/A')}")
                print(f"     - Documents: {collection.get('documents', 0)}")
                print(f"     - Created: {collection.get('created_at', 'N/A')}")
                print()
        else:
            print("ℹ️  No collections found")

        # Test creating a new collection
        print("📝 Test: Creating a new test collection")
        test_collection_name = f"test-collection-{int(time.time())}"
        new_collection = api.create_collection(
            test_collection_name, "Test collection created by Python client", "private"
        )

        if new_collection.get("id"):
            print(
                f"✅ Successfully created collection: {test_collection_name} (ID: {new_collection['id']})"
            )

            # Test getting the specific collection
            print("🔍 Test: Getting specific collection")
            retrieved_collection = api.get_collection(new_collection["id"])
            print(f"✅ Retrieved collection: {retrieved_collection['name']}")

            # Test updating the collection
            print("✏️  Test: Updating collection")
            api.update_collection(
                new_collection["id"], description="Updated test collection description"
            )
            print("✅ Successfully updated collection")

            # Test deleting the collection
            print("🗑️  Test: Deleting collection")
            api.delete_collection(new_collection["id"])
            print("✅ Successfully deleted collection")
        else:
            print("❌ Failed to create collection")

        api.close()
        print("\n✅ Collections test completed successfully!")

    except Exception as e:
        print(f"❌ Collections Test Error: {e}")


def test_documents() -> None:
    """Test documents endpoint."""
    print("🧪 Testing Documents Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get existing documents
        print("\n📋 Getting existing documents:")
        documents = api.get_documents()

        if documents.get("data"):
            for i, document in enumerate(documents["data"], 1):
                print(f"  {i}. {document['name']} (ID: {document['id']})")
                print(f"     - Collection ID: {document.get('collection_id', 'N/A')}")
                print(f"     - Chunks: {document.get('chunks', 0)}")
                print(f"     - Created: {document.get('created_at', 'N/A')}")
                print()
        else:
            print("ℹ️  No documents found")

        # Test getting a specific document if available
        if documents.get("data"):
            first_doc = documents["data"][0]
            print(f"🔍 Test: Getting specific document (ID: {first_doc['id']})")
            document_details = api.get_document(first_doc["id"])
            print(f"✅ Retrieved document: {document_details['name']}")

            # Test getting chunks for this document
            print("📄 Test: Getting document chunks")
            chunks = api.get_chunks(first_doc["id"], limit=3)

            if chunks.get("data"):
                print(f"✅ Found {len(chunks['data'])} chunks")
                for chunk in chunks["data"]:
                    content_preview = chunk.get("content", "")[:100]
                    print(f"  Chunk {chunk['id']}: {content_preview}...")
            else:
                print("ℹ️  No chunks found for this document")
        else:
            print("ℹ️  No documents available for testing")

        api.close()
        print("\n✅ Documents test completed successfully!")

    except Exception as e:
        print(f"❌ Documents Test Error: {e}")


def test_search() -> None:
    """Test search endpoint."""
    print("🧪 Testing Search Endpoint")
    print("=" * 50)

    try:
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get collections for search
        print("\n🔍 Getting collections for search:")
        collections = api.get_collections()

        if collections.get("data"):
            collection_ids = [c["id"] for c in collections["data"]]
            print(
                f"Found {len(collection_ids)} collections: {', '.join(map(str, collection_ids))}"
            )

            # Test search
            print("\n🔍 Test: Searching in collections")
            search_query = "artificial intelligence"
            search_results = api.search(
                search_query, collection_ids, k=3, method="semantic"
            )

            if search_results.get("data"):
                print(
                    f"✅ Found {len(search_results['data'])} search results for '{search_query}':"
                )
                for i, result in enumerate(search_results["data"], 1):
                    print(f"  {i}. Score: {result.get('score', 0):.3f}")
                    print(f"     - Method: {result.get('method', 'N/A')}")
                    content_preview = result.get("chunk", {}).get("content", "")[:150]
                    print(f"     - Content: {content_preview}...")
                    print()
            else:
                print("ℹ️  No search results found")
        else:
            print("ℹ️  No collections available for search")

        api.close()
        print("\n✅ Search test completed successfully!")

    except Exception as e:
        print(f"❌ Search Test Error: {e}")


def test_all() -> None:
    """Run all tests."""
    print("🧪 Running All Tests")
    print("=" * 50)

    tests: list[tuple] = [
        ("Initialization", test_initialization),
        ("Models", test_models),
        ("Completions", test_completions),
        ("Embeddings", test_embeddings),
        ("Usage", test_usage),
        ("Collections", test_collections),
        ("Documents", test_documents),
        ("Search", test_search),
    ]

    for test_name, test_func in tests:
        print(f"\n🚀 Running {test_name} Test...")
        print("-" * 30)
        test_func()
        print(f"✅ {test_name} Test Completed")

    print("\n🎉 All tests completed!")


def main() -> None:
    """Main function to handle command line arguments and run tests."""
    args: list[str] = sys.argv[1:]

    if "--models" in args:
        test_models()
    elif "--completions" in args:
        test_completions()
    elif "--embeddings" in args:
        test_embeddings()
    elif "--usage" in args:
        test_usage()
    elif "--collections" in args:
        test_collections()
    elif "--documents" in args:
        test_documents()
    elif "--search" in args:
        test_search()
    elif "--all" in args:
        test_all()
    else:
        # Default: run initialization test
        test_initialization()


if __name__ == "__main__":
    main()
