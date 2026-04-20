import requests
hash_url = "https://mempool.space/api/blocks/tip/hash"
# choose an endpoint
hash = requests.get(hash_url)
print(f"Block Hash: {hash.text}")
info_url = f"https://mempool.space/api/block/{hash.text}"
response = requests.get(info_url)
data = response.json()
list = ["height", "difficulty", "nonce", "tx_count"]
for i in list:
    print(f"{i}: {data[i]}")