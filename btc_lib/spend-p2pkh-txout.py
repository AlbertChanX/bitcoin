#coding:utf-8
import hashlib
from bitcoin import SelectParams
from bitcoin.core import b2x, b2lx, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

from btc_lib import walletinfo

SelectParams('testnet')

# Create the (in)famous correct brainwallet secret key.
# h = hashlib.sha256(b'correct horse battery staple').digest()
# seckey = CBitcoinSecret.from_secret_bytes(h)


# CMutableTxIn list
def create_txin(amounts):
    us_list, blc = walletinfo.get_txin(amounts)

    txin = []
    for us in us_list:
        txin.append(CMutableTxIn(COutPoint(lx(us.txid), us.vout)))
        print(us.txid)
    return txin,blc


# Create the txout. This time we create the scriptPubKey from a Bitcoin address.
# amounts is dic

# CMutableTxOut list
def create_txout(ads_amt):
    txout = []
    for k, v in ads_amt.items():
        txout.append(CMutableTxOut(v*COIN, CBitcoinAddress(k).to_scriptPubKey()))
    return txout


# Create the unsigned transaction.   txin---》list
def create_tx(txin, txout):
    tx = CMutableTransaction(txin, txout)
    # print('tx-length: ', len(tx.serialize()) / 2)
    return tx


# 多个 txin  sign
# Calculate the signature hash for that transaction.
def sign_tx(txin, tx):
    for n, ti in enumerate(txin):
        txid = b2lx(ti.prevout.hash)
        vout = ti.prevout.n
        # print('txid: ', txid, vout)
        seckey = walletinfo.get_seckeybytxid(txid, vout)
        # print(seckey)
        seckey = CBitcoinSecret(seckey)
        # We also need the scriptPubKey of the output we're spending
        txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])
        sighash = SignatureHash(txin_scriptPubKey, tx, n, SIGHASH_ALL)
        # Now sign it.
        sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
        ti.scriptSig = CScript([sig, seckey.pub])
        # print(VerifyScript(ti.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,)))
    return b2x(tx.serialize())   #tx_hex


if __name__ == "__main__":
    to_address = 'mt75PpVcfjceTcCn1C8qgJr4ext2F31udd'
    ads_amt = dict()
    ads_amt.setdefault(to_address, 3.23)
    ads_amt.setdefault('miEJxBRNmpVVrybtvsLwxeCxcmypdXQYDD', 0.1)
    # 发送总额
    amounts = 0
    for k, v in ads_amt.items():
        amounts += v
    print('amounts :', amounts)
    # 根据发送金额，返回输入和多余的输入
    txin, blc = create_txin(amounts)
    print('balance :', blc)
    print('txin: %s' % (txin))
    #------------------------------

    # 查看是否需要找零
    back = walletinfo.get_back(blc, txin, ads_amt)
    if back:
        a = walletinfo.get_address()   # back　to who???
        ads_amt.setdefault(a, back)
    print(ads_amt)

    # {address:amount}   创建输出
    txout = create_txout(ads_amt)

    # 创建交易
    tx = create_tx(txin, txout)
    print('txsize : ', len(b2x(tx.serialize()))/2)   # 未签名的交易大小  235  ---> 238

    # sign
    tx_hex = sign_tx(txin, tx)     # tx hex   106*x    3*106=318   318+235=553

    # fee
    print(len(tx_hex)/2)     # 费用比这里高  1-2 satoshi   554 + 2 = 556 = 3*106 + 238
    #send
    print(walletinfo.send_tx(tx_hex))   # txid




