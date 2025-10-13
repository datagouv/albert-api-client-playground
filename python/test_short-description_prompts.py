#!/usr/bin/env python3
"""
Test prompts related to resources on data.gouv.fr API

This script tests various prompts and interactions with data.gouv.fr API resources.
"""

import json
from pathlib import Path
import httpx
from dotenv import load_dotenv
from albert_api import AlbertAPI

load_dotenv()

DATAGOUV_API_BASE_URL = "https://www.data.gouv.fr/api/1/"


def load_prompts(prompts_file: Path | str = "prompts.json") -> list[dict]:
    """Load prompts from JSON file.

    Args:
        prompts_file: Path to the prompts JSON file

    Returns:
        List of prompt templates
    """
    prompts_path = Path(prompts_file)
    return json.loads(prompts_path.read_text(encoding="utf-8"))


def interpolate_prompt(
    prompt_name: str,
    description_short_max_length: int,
    title: str,
    description: str,
    organization_name: str,
    prompts_file: Path | str = "prompts.json",
) -> list[dict]:
    """Load a prompt template and interpolate variables.

    Args:
        prompt_name: Name of the prompt in the JSON file
        description_short_max_length: Max length for short descriptions
        title: Dataset title
        description: Description text
        organization_name: Organization name
        prompts_file: Path to the prompts JSON file

    Returns:
        List of messages with interpolated content
    """
    prompts = load_prompts(prompts_file)

    # Find prompt by name
    prompt_template = None
    for prompt in prompts:
        if prompt.get("name") == prompt_name:
            prompt_template = prompt
            break

    if prompt_template is None:
        available_prompts = [p.get("name") for p in prompts]
        raise ValueError(
            f"Prompt '{prompt_name}' not found in {prompts_file}. Available prompts: {available_prompts}"
        )

    messages = []

    for message in prompt_template["messages"]:
        content = message["content"]
        # Replace all variables
        content = content.replace(
            "${description_short_max_length}", str(description_short_max_length)
        )
        content = content.replace("${description}", description)
        content = content.replace("${title}", title)
        content = content.replace("${organization_name}", organization_name)

        messages.append({"role": message["role"], "content": content})

    return messages


def get_dataset_info(dataset_id: str) -> tuple[str | None, str | None, str | None]:
    dataset_url = f"{DATAGOUV_API_BASE_URL}/datasets/{dataset_id}/"

    # Create httpx client and make the request
    with httpx.Client() as client:
        response = client.get(dataset_url, headers={"accept": "application/json"})

        response.raise_for_status()
        data = response.json()

        # Extract dataset information
        title = data.get("title")
        description = data.get("description")
        organization_name = data.get("organization", {}).get("name")

        return (title, description, organization_name)


def main() -> None:
    datasets_path = Path("datasets.json")
    dataset_ids: list[str] = json.loads(datasets_path.read_text(encoding="utf-8"))

    api = AlbertAPI()
    
    # Get available models
    models = api.get_models()
    text_models = [m for m in models.get("data", []) if m["type"] == "text-generation"]
    if not text_models:
        print("No text-generation models available")
        return
    model = text_models[0]["id"]
    print(f"Using model: {model}\n")

    for dataset_id in dataset_ids:
        print(f"\n{'=' * 80}")
        print(f"Dataset: {dataset_id}")
        print("=" * 80)

        try:
            title, description, organization_name = get_dataset_info(dataset_id)
            print(f"Title: {title}")
            print(f"Organization: {organization_name}")
            print(f"Description length: {len(description)}")

            messages = interpolate_prompt(
                "antonin1_fallback",
                description_short_max_length=200,
                title=title,
                description=description,
                organization_name=organization_name,
            )

            response = api.chat_completions(messages, model)
            short_description = response["choices"][0]["message"]["content"]

            print(f"\nGenerated short description:\n{short_description}")
            print(f"Characters: {len(short_description)}")

        except Exception as e:
            print(f"Error: {e}")

    api.close()


if __name__ == "__main__":
    main()
