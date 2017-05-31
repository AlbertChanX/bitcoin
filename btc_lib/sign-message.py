# coding:utf-8
#from sign-message.py
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
import bitcoin
# bitcoin.SelectParams('testnet')
key = CBitcoinSecret("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG")
print key.pub
# pk--> address
address = P2PKHBitcoinAddress.from_pubkey(key.pub)  # "1F26pNMrywyZJdr22jErtKcjF8R3Ttt55G"
message = "Hey I just met you, and this is crazy, but I'll verify my address, maybe ..."

message = BitcoinMessage(message)
print type(message)

# key + message --> sig
signature = SignMessage(key, message)

print(key, address)
print("Address: %s" % address)
print("Message: %s" % message)
print("\nSignature: %s" % signature)
###return True or False


print("\nVerified: %s" % VerifyMessage(address, message, signature))

print("\nTo verify using bitcoin core;")
print("`bitcoin-cli verifymessage %s \"%s\" \"%s\"`" % (address, signature.decode('ascii'), message))