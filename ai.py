from __future__ import annotations

from functools import lru_cache

import ollama

EMBED_MODEL = 'mxbai-embed-large'

@lru_cache(maxsize=2048)
def get_embedding(text: str) -> list[float]:
  """
    Returns an embedding vector for the given text using a local Ollama model.

    Notes:
    - Uses a small LRU cache to avoid re-embedding repeated queries.
    - Raises ValueError for empty input.
    - Raises RuntimeError if the model call fails.
  """
  if text is None:
    raise ValueError("text cannot be None")
  
  text = text.strip()
  if not text:
    raise ValueError("text cannot be empty")
  
  try:
    # resp = ollama.embeddings(model=EMBED_MODEL, prompt=text) deprecated in favour of embed
    resp = ollama.embed(model=EMBED_MODEL, input=text)
    emb = resp.get("embedding")
    if not emb:
      raise RuntimeError("No embedding returned from Ollama.")
    return emb
  except Exception as e:
    raise RuntimeError(f"Ollama embedding failed: {e}") from e
  
def build_offer_text(restaurant_name: str, food_name: str, quantity: int, description: str | None, location: str) -> str:
    """
    Creates a consistent text representation of an offer for embedding.
    """
    parts = [
        f"food: {food_name}",
        f"quantity: {quantity}",
        f"location: {location}",
        f"restaurant: {restaurant_name}",
    ]
    if description:
        parts.append(f"description: {description}")
    return " | ".join(parts)