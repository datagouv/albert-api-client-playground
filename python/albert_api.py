#!/usr/bin/env python3
"""
Albert API Python Client

A comprehensive Python client for interacting with the Albert API.
Based on the OpenAPI 3.1.0 specification.

Documentation:
- API Documentation: https://albert.api.etalab.gouv.fr/documentation
- Swagger UI: https://albert.api.etalab.gouv.fr/swagger

Environment Variables:
- ALBERT_API_BASE_URL: Base URL for the Albert API
- ALBERT_API_KEY: API key for authentication
"""

import os
import httpx
import json
from pathlib import Path


class AlbertAPI:
    """
    Albert API Client

    A comprehensive client for interacting with the Albert API, providing access to:
    - Chat completions
    - Embeddings
    - Document processing and search
    - Audio transcription
    - OCR and parsing
    - Collections and documents management
    - Usage tracking
    - Token management

    Documentation:
    - API Documentation: https://albert.api.etalab.gouv.fr/documentation
    - Swagger UI: https://albert.api.etalab.gouv.fr/swagger
    """

    def __init__(
        self, base_url: str | None = None, api_key: str | None = None, timeout: int = 30
    ) -> None:
        """
        Initialize the Albert API client.

        Args:
            base_url: Base URL for the API (defaults to ALBERT_API_BASE_URL env var)
            api_key: API key for authentication (defaults to ALBERT_API_KEY env var)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or os.getenv("ALBERT_API_BASE_URL")
        self.api_key = api_key or os.getenv("ALBERT_API_KEY")
        self.timeout = timeout

        if not self.base_url:
            raise ValueError(
                "Base URL is required. Set ALBERT_API_BASE_URL environment variable or pass base_url parameter."
            )
        if not self.api_key:
            raise ValueError(
                "API key is required. Set ALBERT_API_KEY environment variable or pass api_key parameter."
            )

        self.session = httpx.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make a request to the Albert API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            API response as dictionary

        Raises:
            RuntimeError: If the request fails
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method, url=url, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()

            # Handle empty responses
            if response.status_code == 204:
                return {}

            return response.json()

        except httpx.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON response: {e}")

    # ============================================================================
    # MODELS
    # ============================================================================

    def get_models(self) -> dict:
        """
        Get list of available models.

        Returns:
            Dictionary containing available models
        """
        return self._make_request("GET", "/v1/models")

    def get_model(self, model: str) -> dict:
        """
        Get information about a specific model.

        Args:
            model: Model name/ID

        Returns:
            Model information
        """
        return self._make_request("GET", f"/v1/models/{model}")

    def get_models_ids(self) -> list[str]:
        """Get the list of the official names for all the available Albert models."""
        try:
            models = self.get_models()
            return [m["id"] for m in models.get("data", [])]
        except Exception as e:
            print(f"Unable to get the list of Albert models: {str(e)}")
            return []

    # ============================================================================
    # CHAT COMPLETIONS
    # ============================================================================

    def chat_completions(self, messages: list[dict], model: str, **kwargs) -> dict:
        """
        Create a chat completion.

        Args:
            messages: List of message dictionaries
            model: Model to use for completion
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Chat completion response
        """
        data = {"messages": messages, "model": model, **kwargs}
        return self._make_request("POST", "/v1/chat/completions", json=data)

    def agents_completions(self, messages: list[dict], model: str, **kwargs) -> dict:
        """
        Create an agent completion with MCP bridge tools.

        Args:
            messages: List of message dictionaries
            model: Model to use for completion
            **kwargs: Additional parameters

        Returns:
            Agent completion response
        """
        data = {"messages": messages, "model": model, **kwargs}
        return self._make_request("POST", "/v1/agents/completions", json=data)

    def get_agents_tools(self) -> dict:
        """
        Get available tools for agents.

        Returns:
            Available tools
        """
        return self._make_request("GET", "/v1/agents/tools")

    # ============================================================================
    # EMBEDDINGS
    # ============================================================================

    def create_embeddings(
        self, input_text: str | list[str], model: str, **kwargs
    ) -> dict:
        """
        Create embeddings for text.

        Args:
            input_text: Text or list of texts to embed
            model: Embedding model to use
            **kwargs: Additional parameters

        Returns:
            Embeddings response
        """
        data = {"input": input_text, "model": model, **kwargs}
        return self._make_request("POST", "/v1/embeddings", json=data)

    # ============================================================================
    # AUDIO TRANSCRIPTION
    # ============================================================================

    def transcribe_audio(self, file_path: str | Path, model: str, **kwargs) -> dict:
        """
        Transcribe audio file.

        Args:
            file_path: Path to audio file
            model: Transcription model to use
            **kwargs: Additional parameters (language, response_format, etc.)

        Returns:
            Transcription response
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        data = {"model": model, **kwargs}

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "audio/mpeg")}
            return self._make_request(
                "POST", "/v1/audio/transcriptions", data=data, files=files
            )

    # ============================================================================
    # DOCUMENT PROCESSING
    # ============================================================================

    def parse_document(self, file_path: str | Path, **kwargs) -> dict:
        """
        Parse a document (PDF, etc.).

        Args:
            file_path: Path to document file
            **kwargs: Additional parameters (output_format, force_ocr, etc.)

        Returns:
            Parsed document response
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document file not found: {file_path}")

        data = kwargs

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/pdf")}
            return self._make_request("POST", "/v1/parse-beta", data=data, files=files)

    def ocr_document(self, file_path: str | Path, model: str, **kwargs) -> dict:
        """
        Extract text from PDF using OCR.

        Args:
            file_path: Path to PDF file
            model: OCR model to use
            **kwargs: Additional parameters (dpi, prompt, etc.)

        Returns:
            OCR response
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        data = {"model": model, **kwargs}

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/pdf")}
            return self._make_request("POST", "/v1/ocr-beta", data=data, files=files)

    # ============================================================================
    # COLLECTIONS AND DOCUMENTS
    # ============================================================================

    def create_collection(
        self, name: str, description: str | None = None, visibility: str = "private"
    ) -> dict:
        """
        Create a new collection.

        Args:
            name: Collection name
            description: Collection description
            visibility: Collection visibility (private/public)

        Returns:
            Created collection response
        """
        data = {"name": name, "description": description, "visibility": visibility}
        return self._make_request("POST", "/v1/collections", json=data)

    def get_collections(self, offset: int = 0, limit: int = 10) -> dict:
        """
        Get list of collections.

        Args:
            offset: Pagination offset
            limit: Number of collections to return

        Returns:
            Collections list
        """
        params = {"offset": offset, "limit": limit}
        return self._make_request("GET", "/v1/collections", params=params)

    def get_collection(self, collection_id: int) -> dict:
        """
        Get collection by ID.

        Args:
            collection_id: Collection ID

        Returns:
            Collection information
        """
        return self._make_request("GET", f"/v1/collections/{collection_id}")

    def update_collection(self, collection_id: int, **kwargs) -> None:
        """
        Update collection.

        Args:
            collection_id: Collection ID
            **kwargs: Fields to update (name, description, visibility)
        """
        self._make_request("PATCH", f"/v1/collections/{collection_id}", json=kwargs)

    def delete_collection(self, collection_id: int) -> None:
        """
        Delete collection.

        Args:
            collection_id: Collection ID
        """
        self._make_request("DELETE", f"/v1/collections/{collection_id}")

    def create_document(
        self, file_path: str | Path, collection_id: int, **kwargs
    ) -> dict:
        """
        Create a document in a collection.

        Args:
            file_path: Path to document file
            collection_id: Collection ID
            **kwargs: Additional parameters (chunk_size, output_format, etc.)

        Returns:
            Created document response
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document file not found: {file_path}")

        data = {"collection": collection_id, **kwargs}

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/pdf")}
            return self._make_request("POST", "/v1/documents", data=data, files=files)

    def get_documents(
        self, collection_id: int | None = None, limit: int = 10, offset: int = 0
    ) -> dict:
        """
        Get documents from collection.

        Args:
            collection_id: Collection ID (optional, to filter by collection)
            limit: Number of documents to return
            offset: Pagination offset

        Returns:
            Documents list
        """
        params = {"limit": limit, "offset": offset}
        if collection_id is not None:
            params["collection"] = collection_id

        return self._make_request("GET", "/v1/documents", params=params)

    def get_document(self, document_id: int) -> dict:
        """
        Get document by ID.

        Args:
            document_id: Document ID

        Returns:
            Document information
        """
        return self._make_request("GET", f"/v1/documents/{document_id}")

    def delete_document(self, document_id: int) -> None:
        """
        Delete document.

        Args:
            document_id: Document ID
        """
        self._make_request("DELETE", f"/v1/documents/{document_id}")

    # ============================================================================
    # CHUNKS
    # ============================================================================

    def get_chunks(self, document_id: int, limit: int = 10, offset: int = 0) -> dict:
        """
        Get chunks of a document.

        Args:
            document_id: Document ID
            limit: Number of chunks to return
            offset: Pagination offset

        Returns:
            Chunks list
        """
        params = {"limit": limit, "offset": offset}
        return self._make_request("GET", f"/v1/chunks/{document_id}", params=params)

    def get_chunk(self, document_id: int, chunk_id: int) -> dict:
        """
        Get specific chunk of a document.

        Args:
            document_id: Document ID
            chunk_id: Chunk ID

        Returns:
            Chunk information
        """
        return self._make_request("GET", f"/v1/chunks/{document_id}/{chunk_id}")

    # ============================================================================
    # SEARCH
    # ============================================================================

    def search(
        self, prompt: str, collections: list[int] | None = None, **kwargs
    ) -> dict:
        """
        Search for relevant chunks.

        Args:
            prompt: Search query
            collections: List of collection IDs to search in
            **kwargs: Additional parameters (method, k, score_threshold, etc.)

        Returns:
            Search results
        """
        data = {"prompt": prompt, "collections": collections or [], **kwargs}
        return self._make_request("POST", "/v1/search", json=data)

    # ============================================================================
    # RERANK
    # ============================================================================

    def rerank(self, prompt: str, input_texts: list[str], model: str) -> dict:
        """
        Rerank texts by relevance to prompt.

        Args:
            prompt: Reranking prompt
            input_texts: List of texts to rerank
            model: Reranking model to use

        Returns:
            Reranking results
        """
        data = {"prompt": prompt, "input": input_texts, "model": model}
        return self._make_request("POST", "/v1/rerank", json=data)

    # ============================================================================
    # USAGE
    # ============================================================================

    def get_usage(self, limit: int = 50, page: int = 1, **kwargs) -> dict:
        """
        Get account usage information.

        Args:
            limit: Number of records per page
            page: Page number
            **kwargs: Additional parameters (order_by, order_direction, date_from, date_to)

        Returns:
            Usage information
        """
        params = {"limit": limit, "page": page, **kwargs}
        return self._make_request("GET", "/v1/usage", params=params)

    # ============================================================================
    # TOKEN MANAGEMENT
    # ============================================================================

    def create_token(
        self, name: str, user: int | None = None, expires_at: int | None = None
    ) -> dict:
        """
        Create a new token.

        Args:
            name: Token name
            user: User ID (optional, for admin use)
            expires_at: Expiration timestamp (optional)

        Returns:
            Created token response
        """
        data = {"name": name}
        if user is not None:
            data["user"] = user
        if expires_at is not None:
            data["expires_at"] = expires_at

        return self._make_request("POST", "/tokens", json=data)

    def get_tokens(self, offset: int = 0, limit: int = 10, **kwargs) -> dict:
        """
        Get list of tokens.

        Args:
            offset: Pagination offset
            limit: Number of tokens to return
            **kwargs: Additional parameters (order_by, order_direction)

        Returns:
            Tokens list
        """
        params = {"offset": offset, "limit": limit, **kwargs}
        return self._make_request("GET", "/tokens", params=params)

    def get_token(self, token_id: int) -> dict:
        """
        Get token by ID.

        Args:
            token_id: Token ID

        Returns:
            Token information
        """
        return self._make_request("GET", f"/tokens/{token_id}")

    def delete_token(self, token_id: int) -> None:
        """
        Delete token.

        Args:
            token_id: Token ID
        """
        self._make_request("DELETE", f"/tokens/{token_id}")

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
