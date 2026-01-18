from __future__ import annotations

from functools import lru_cache
from typing import Any, Iterable

import numpy as np
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
    embeddings = resp.get("embeddings")
    if not embeddings or not isinstance(embeddings, list) or len(embeddings) == 0:
        raise RuntimeError("No embeddings returned from Ollama.")
    return embeddings[0]

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


def cosine_similarity(query_vec: list[float], db_vec: list[float]) -> float:
  q = np.array(query_vec, dtype=np.float32)
  d = np.array(db_vec, dtype=np.float32)

  qn = np.linalg.norm(q)
  dn = np.linalg.norm(d)

  if qn == 0.0 or dn == 0.0:
    return 0.0
  
  return float(np.dot(q, d) / (qn * dn))

def semantic_rank_offers(
    query: str,
    offers: Iterable[Any],
    top_k: int = 5,
    threshold: float = 0.5
) -> list[tuple[float, Any]]:
  q_emb = get_embedding(query)

  scored: list[tuple[float, Any]] = []
  for offer in offers:
    if not offer.embedding:
      continue
    score = cosine_similarity(q_emb, offer.embedding)
    if score >= threshold:
      scored.append((score, offer))
  scored.sort(key = lambda x: x[0], reverse=True)
  return scored[:top_k]