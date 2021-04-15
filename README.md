# python-hd-wallet-scanner

A HD Wallet scanner that searches hash160 addresses from the top 100000 bitcoin addresses in a bloom filter with a positive balance looking for a collision, when a collision is found the script will provide you with xprv, xpub, wif and address.

dotenv file to add details so that you can receive alerts in a discord webhook or on pushover when collision is found

![alt text](https://i.imgur.com/ksINotd.png)

Source code above, this is my first project so be nice :)

Binaries available for download for those without Python 3.9 - Comes with pre-generated bloom filter
https://github.com/AFedelmid/python-hd-wallet-scanner/releases/tag/1

# Creating a bloom filter

Download every Bitcoin address with a positive balance from https://bitkeys.work/download.php

in linux or WSL on Windows extract the first column of that csv: cut -d, -f 1 btc_balance_sorted.csv > all_btc_addr.txt

add all_btc_addr.bin to your bloom filter search, The bloom filter will take a little time to generate as there is over 31m addresses.
