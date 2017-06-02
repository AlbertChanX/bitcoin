# coding:utf-8

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
from decimal import Decimal
# logging.basicConfig()
# logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

rpc_user = 'bitcoin'
rpc_password = '123456'

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(rpc_user, rpc_password))
rpc_connection.walletpassphrase('cyc123', 60)

def numto8(x):
    return Decimal(x).quantize(Decimal('0.00000000'))

def get_seckeybyaddress(address):
    return rpc_connection.dumpprivkey(address)

def get_seckeybytxid(txid, vout):
    us = get_us()
    key = ''
    for i in us:
        if i['txid'] == txid and i['vout'] == vout:
            key = get_seckeybyaddress(i['address'])
            break
    return key


class Unspent(object):
    def __init__(self, txid, vout, address, amount):
        self.txid = txid
        self.vout = vout
        self.address = address
        self.amount = amount
    def __repr__(self):
        return "<%s:%s with %s>"%(self.address, self.vout, self.amount)

# get proper txin
def get_txin(amounts):
    lus = rpc_connection.listunspent()
    balance = 0
    for i in lus:
        balance += i['amount']
    if balance < amounts:
        raise ValueError('out of balance!')
    else:
        us = [Unspent(i['txid'], i['vout'], i['address'], i['amount']) for i in lus]
        #from small -->
        us.sort(key=lambda unspent: unspent.amount)
        # print(us)
        tmp = 0
        index = 0
        for i, j in enumerate(us):
            tmp += j.amount
            if tmp > amounts:
                index = i + 1
                break
        blc = tmp - numto8(amounts)
        return us[slice(index)], blc

def get_back(balance, inputs, outputs, fee = 0.00001):
    txin_num = len(inputs)
    txout_num = len(outputs)
    ###计算fee   148   34
    tx_bytes = (4 + 4 + 1 + 1 + txin_num * (106 + 32 + 4 + 4 + 1 + 1) + txout_num * (25 + 8 + 1))
    all_fee = tx_bytes / 1000.0 * fee
    print('allfee :', numto8(all_fee))
    back = balance - numto8(all_fee)
    bk = back - numto8(34/1000.0*fee)
    if bk > 0:
        print(bk)
        return bk
    else:
        return False

# get txin's amounts
def get_amounts(us):
    amounts = 0
    for i in us:
        amounts += i.amount
    return amounts

# print(get_amounts(get_txin(8)))
def get_address():
    return rpc_connection.getnewaddress()

def get_us():
    return rpc_connection.listunspent()
def send_tx(hex):
    # tx hash in hex
    return rpc_connection.sendrawtransaction(hex)

def decode(hex):
    return rpc_connection.decodescript(hex)