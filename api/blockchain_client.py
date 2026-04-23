"""
Blockchain API client.

Provides helper functions to fetch blockchain data from public APIs.
"""

import requests

BASE_URL = "https://blockchain.info"
MEMPOOL_BASE_URL = "https://mempool.space/api"

def get_latest_block() -> dict:
    """Return the latest block summary."""
    response = requests.get(f"{BASE_URL}/latestblock", timeout=10)
    response.raise_for_status()
    return response.json()

def get_block(block_hash: str) -> dict:
    """Return full details for a block identified by *block_hash*."""
    response = requests.get(
        f"{BASE_URL}/rawblock/{block_hash}", timeout=10
    )
    response.raise_for_status()
    return response.json()

def get_difficulty_history(n_points: int = 100) -> list[dict]:
    """Return the last *n_points* difficulty values as a list of dicts."""
    response = requests.get(
        f"{BASE_URL}/charts/difficulty",
        params={"timespan": "1year", "format": "json", "sampled": "true"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("values", [])[-n_points:]

def get_latest_block_hash() -> str:
    """Fetch the latest block hash from the Mempool API."""
    response = requests.get(f"{MEMPOOL_BASE_URL}/blocks/tip/hash", timeout=10)
    response.raise_for_status()
    return response.text

def get_block_details_from_mempool(block_hash: str) -> dict:
    """Fetch block details from the Mempool API using the block hash."""
    response = requests.get(f"{MEMPOOL_BASE_URL}/block/{block_hash}", timeout=10)
    response.raise_for_status()
    return response.json()
