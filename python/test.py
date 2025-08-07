#!/usr/bin/env python3
"""
Albert API Python Client - Testing and Demo

This script demonstrates how to use the AlbertAPI client.
Run this to test the API functionality.

Usage:
    python test.py
"""

import os
from dotenv import load_dotenv
from albert_api import AlbertAPI

# Load environment variables from .env file for testing
load_dotenv()


def main() -> None:
    """Main function demonstrating Albert API usage."""
    print("🚀 Albert API Playground")
    print("=" * 50)

    # Check if API key is available
    if not os.getenv("ALBERT_API_KEY"):
        print("❌ ALBERT_API_KEY environment variable is not set!")
        print("Please set it with: export ALBERT_API_KEY='your-api-key'")
        print("\nExample usage:")
        print("  export ALBERT_API_KEY='your-api-key-here'")
        print("  python main.py")
        return

    try:
        # Initialize the API client
        api = AlbertAPI()
        print("✅ Albert API client initialized successfully!")

        # Get available models
        print("\n🔍 Available Models:")
        models = api.get_models()
        for model in models.get("data", [])[:3]:  # Show first 3 models
            print(f"  - {model['id']} ({model['type']})")

        # Simple chat completion example
        print("\n💬 Simple Chat Example:")
        messages = [{"role": "user", "content": "Dis-moi bonjour en français!"}]

        # Use the first available text-generation model
        text_models = [
            m for m in models.get("data", []) if m["type"] == "text-generation"
        ]
        if text_models:
            model_name = text_models[0]["id"]
            response = api.chat_completions(
                messages=messages,
                model=model_name,
                max_completion_tokens=50,
                temperature=0.7,
            )

            if response.get("choices"):
                content = response["choices"][0]["message"]["content"]
                print(f"🤖 Response: {content}")
            else:
                print("❌ No response received")
        else:
            print("ℹ️  No text-generation models available")

        # Get usage information
        print("\n📊 Usage Information:")
        usage = api.get_usage(limit=1)
        print(f"  Total requests: {usage.get('total_requests', 0)}")
        print(f"  Total tokens: {usage.get('total_tokens', 0)}")
        print(f"  Total CO2: {usage.get('total_co2', 0)} grams")

        api.close()
        print("\n✅ Demo completed successfully!")

    except RuntimeError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
