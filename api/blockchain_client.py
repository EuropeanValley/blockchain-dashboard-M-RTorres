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

def get_block_history(time_period: str = "All") -> dict:
    """Return difficulty and hashrate data for the specified time period.

    Args:
        time_period (str): The trailing time period for the data. Valid values are
            '1m', '3m', '6m', '1y', '2y', '3y' or 'All' for all time. Defaults to 'All'.

    Returns:
        dict: A dictionary containing historical hashrates, difficulty, current hashrate,
            and current difficulty.
    """

    if time_period not in ["1m", "3m", "6m", "1y", "2y", "3y", "All"]:
        raise ValueError(f"{time_period} is an invalid time period. Valid values are '1m', '3m', '6m', '1y', '2y', '3y' or 'All'.")

    if time_period == "All":
        time_period = ""
    else:
        time_period = f"/{time_period}"

    response = requests.get(
        f"{MEMPOOL_BASE_URL}/v1/mining/hashrate{time_period}",
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    return {
        "hashrates": data.get("hashrates", []),
        "difficulty": data.get("difficulty", []),
        "height": data.get("height", []),
        "currentHashrate": data.get("currentHashrate"),
        "currentDifficulty": data.get("currentDifficulty"),
    }

def get_time_between_blocks(amount_of_blocks: int = 5) -> list[dict]:
    time_differences = []
    current_block = get_latest_block()
    for _ in range(amount_of_blocks):
        previous_block_hash = current_block.get("previousblockhash")
        if not previous_block_hash:
            break
        previous_block = get_block(previous_block_hash)
        time_diff = current_block["timestamp"] - previous_block["timestamp"]
        time_differences.append({
            "height": current_block["height"],
            "time_difference": time_diff,
        })
        current_block = previous_block
    return time_differences