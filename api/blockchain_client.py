"""
Blockchain API client.

Provides helper functions to fetch blockchain data from public APIs.
"""

import requests

BASE_URL = "https://blockchain.info"
MEMPOOL_BASE_URL = "https://mempool.space/api"

def get_latest_block() -> dict:
    """Return the latest block summary."""
    response = requests.get(f"{MEMPOOL_BASE_URL}/blocks/tip", timeout=10)
    response.raise_for_status()
    return response.json()[1]

def get_block(block_hash: str) -> dict:
    """Return full details for a block identified by *block_hash*."""
    response = requests.get(
        f"{MEMPOOL_BASE_URL}/block/{block_hash}", timeout=10
    )
    response.raise_for_status()
    return response.json()

def get_block_history(time_period: str = "") -> dict:
    """Return difficulty and hashrate data for the specified time period.

    Args:
        time_period (str): The trailing time period for the data. Valid values are
            '1m', '3m', '6m', '1y', '2y', '3y' or '' for all time. Defaults to ''.

    Returns:
        dict: A dictionary containing historical hashrates, difficulty, current hashrate,
            and current difficulty.
    """
    response = requests.get(
        f"{MEMPOOL_BASE_URL}/v1/mining/hashrate/{time_period}",
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    return {
        "hashrates": data.get("hashrates", []),
        "difficulty": data.get("difficulty", []),
        "currentHashrate": data.get("currentHashrate"),
        "currentDifficulty": data.get("currentDifficulty"),
    }

def get_time_between_blocks(amount_of_blocks: int = None) -> list[dict]:
    """Return the time between blocks in the specified height range.

    Args:
        amount_of_blocks (int, optional): The number of blocks to consider. Defaults to None.

    Returns:
        list[dict]: A list of dictionaries containing block heights and time differences.
    """

    url = f"{MEMPOOL_BASE_URL}/v1/blocks-bulk/{amount_of_blocks}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    blocks = response.json()

    time_differences = []
    for i in range(1, len(blocks)):
        time_diff = blocks[i]["timestamp"] - blocks[i - 1]["timestamp"]
        time_differences.append({
            "height": blocks[i]["height"],
            "time_difference": time_diff,
        })

    return time_differences