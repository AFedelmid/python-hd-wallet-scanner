from py_crypto_hd_wallet import HdWalletFactory, HdWalletCoins, HdWalletWordsNum, HdWalletDataTypes, HdWalletKeyTypes
from bloomfilter import BloomFilter
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import datetime
from pushover import Client
import requests
from dotenv import load_dotenv
import os
from Crypto.Hash import SHA256, RIPEMD160
import binascii

load_dotenv()

client = Client(os.getenv("POCLIENT"), api_token=os.getenv("POAPI"))
start_time = time.time()

def main():
    print("HD Wallet Scan Started")
    print("Loading Bloom Filter")
    bloom_filter = loadBloomFilter()
    print("Bloom Filter Loaded")
    print("Testing Addresses")
    print("--------------------")
    testAddress(bloom_filter)

def testAddress(bloom_filter):
    keyCount = 0
    keyFound = 0
    while True:
        keyList = []
        hd_wallet_fact = HdWalletFactory(HdWalletCoins.BITCOIN)
        hd_wallet = hd_wallet_fact.CreateRandom("my_wallet_name", HdWalletWordsNum.WORDS_NUM_12)
        hd_wallet.Generate(addr_num=50)
        addresses = hd_wallet.GetData(HdWalletDataTypes.ADDRESSES)
        for addr in addresses:
            hash160 = createHash160(addr.GetKey(HdWalletKeyTypes.RAW_COMPR_PUB))
            if hash160 in bloom_filter:
                r = requests.get("https://blockchain.info/q/addressbalance/{}".format(addr.GetKey(HdWalletKeyTypes.ADDRESS)))
                #print("https://blockchain.info/q/addressbalance/{}".format(addr.GetKey(HdWalletKeyTypes.ADDRESS)))
                if r.text == "0" or r.text == "Invalid Bitcoin Address":
                    #print("{} - {}, {}, {}".format(r.text, addr.GetKey(HdWalletKeyTypes.ADDRESS), addr.GetKey(HdWalletKeyTypes.EX_PRIV), addr.GetKey(HdWalletKeyTypes.WIF_PRIV)))
                    continue
                else:
                    print("Found: {} - {}".format(addr.GetKey(HdWalletKeyTypes.ADDRESS), r.text))
                    keyList.append(addr.GetKey(HdWalletKeyTypes.EX_PRIV))
                    keyList.append(addr.GetKey(HdWalletKeyTypes.EX_PUB))
                    keyList.append(addr.GetKey(HdWalletKeyTypes.ADDRESS))
                    keyList.append(addr.GetKey(HdWalletKeyTypes.WIF_PRIV))
                    keyList.append(r.text)
                    sendDiscordWebhook(keyList)
                    poMessage = "XPRV: {}, XPUB: {}, ADDR: {}, WIF: {}, BAL: {}".format(keyList[0], keyList[1], keyList[2], keyList[3], keyList[4])
                    client.send_message(poMessage, title="BloomFilter")
                    keyFound += 1
        keyCount += 50
        print("Time: " + createTimer() + " | Keys Checked: {}".format(keyCount) + " | Keys Found: {}".format(keyFound), end='\r')

def createTimer():
    sec = time.time() - start_time
    timer = str(datetime.timedelta(seconds=round(sec)))
    return timer

def createHash160(publickey):
    pub = bytes.fromhex(publickey)
    sha256Hash = SHA256.new(pub).digest()
    ripemd160Hash = RIPEMD160.new(sha256Hash).digest()
    return binascii.hexlify(ripemd160Hash).decode(encoding="utf-8")

def loadBloomFilter():
    with open("all_btc_addr.bin", "rb") as fp:
        bloom_filter = BloomFilter.load(fp)
    return bloom_filter

def sendDiscordWebhook(addrObj):
    webhook = DiscordWebhook(url=os.getenv("DWH"), username="BloomFilter")

    embed = DiscordEmbed(title='BloomFilter', description='Found Collision', color='03b2f8')
    embed.set_timestamp()
    embed.add_embed_field(name='EX_PRIV', value=f'{addrObj[0]}')
    embed.add_embed_field(name='EX_PUB', value=f'{addrObj[1]}')
    embed.add_embed_field(name='ADDRESS', value=f'{addrObj[2]}')
    embed.add_embed_field(name='WIF', value=f'{addrObj[3]}')
    embed.add_embed_field(name='Balance', value=f'{addrObj[4]}')

    webhook.add_embed(embed)
    webhook.execute()

if __name__ == "__main__":
    main()
