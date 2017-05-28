# coding:utf-8

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

rpc_user = 'bitcoin'
rpc_password = '123456'

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(rpc_user, rpc_password))
print(rpc_connection.getinfo())
rpc_connection.walletpassphrase('cyc123', 60)

def numto8(x):
    return Decimal(x).quantize(Decimal('0.00000000'))


txid = '1e22252acf6daa88f17bd0d3a83b16d98e777f50b4f7959e9ad20689277b3f59'
# info = rpc_connection.getrawtransaction(txid, 1)
# print 'getrawtransaction by txid: ', info


def get_blance(us):
    balance = 0
    for i in us:
        balance += i['amount']
    return balance

### 找零
def get_back(balance, inputs, outputs, fee):
    txin_num = len(inputs)
    txout_num = len(outputs) + 1
    ###计算fee    10 + in * 148 + out * 34
    tx_bytes = (4 + 4 + 1 + 1 + txin_num * (106 + 32 + 4 + 4 + 1 + 1) + txout_num * (25 + 8 + 1))
    print tx_bytes
    all_fee = tx_bytes / 1024.0 * fee
    back = balance - amount - numto8(all_fee)
    print numto8(all_fee)
    return back


def send_btc(address, amount, fee):
    us = rpc_connection.listunspent()   #6-9999999,filter_address)
    if len(us)==0:
        logging.error('unspent is %s'%len(us))
        return None
    balance = get_blance(us)
    if balance <= amount:
        logging.error('Insufficient funds')
        return None
    inputs = us
    outputs = dict()
    outputs.setdefault(address, amount)

    back = get_back(balance, inputs, outputs, fee)
    logging.critical('back %.8f'%back)
    # 设置找零
    outputs.setdefault(us[0]['address'], back)
    logging.critical('outputs is %s'%outputs)
    ### inputs : json array, outputs:json object     outputs ???
    hex = rpc_connection.createrawtransaction(inputs, outputs)
    logging.critical('create_hex: %s'%hex)   ###返回十六进制的字符串

    ### sign
    sign = rpc_connection.signrawtransaction(hex)
    logging.critical('signed hex: %s'%sign['hex'])

    ### send
    tx_hash = rpc_connection.sendrawtransaction(sign['hex'])  #sign['hex'] 带上签名的hex
    return  tx_hash


### gettransaction  get from in-wallet
# tx_info = rpc_connection.getrawtransaction("1e22252acf6daa88f17bd0d3a83b16d98e777f50b4f7959e9ad20689277b3f59",True)
# print tx_info
###decoderawtransaction   -->  inputs,outputs
#decode = rpc_connection.decoderawtransaction(hex)
#print decode




if __name__ == '__main__':
    address = "mt75PpVcfjceTcCn1C8qgJr4ext2F31udd"
    add = 'miEJxBRNmpVVrybtvsLwxeCxcmypdXQYDD'
    amount = 1
    fee = 0.00001  # BTC/kB

    send_btc(address, amount, fee)





# # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
# commands = [ [ "getblockhash", height] for height in range(100) ]
# print commands
# block_hashes = rpc_connection.batch_(commands)
# blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
# block_times = [ block["time"] for block in blocks ]
# print(block_times)




