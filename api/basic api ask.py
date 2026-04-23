import requests
info_url = "https://mempool.space/api/blocks/tip"
response = requests.get(info_url)
data = response.json()[1]
#Height referes to the number of blocks preceding it in the blockchain
#Difficulty refers to the amount of zeros required at the beginning of the block hash for it to be considered valid
#Nonce refer to the value that miners can modify in order to change the hash to find one that meets the difficulty requirement
#Tx_count refers to the number of transactions included in the block
list = ["id", "height", "difficulty", "nonce", "tx_count"]
for i in list:
    print(f"{i}: {data[i]}")