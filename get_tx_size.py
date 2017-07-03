# coding:utf-8
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user = 'bitcoin'
rpc_password = '123456'
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(rpc_user, rpc_password))
print(rpc_connection.getinfo())
rpc_connection.walletpassphrase('cyc123', 60)

txid = 'bfd1d80b6b2928e9d3be9ee577113cde28bc341ee1517fe868db7e5abb550559'
rt = rpc_connection.getrawtransaction(txid, 1)
print rt
vin = ''
out = ''
for i in rt['vin']:

    vin = vin + i['scriptSig']['hex']
    #print
    print len(vin)/2
for i in rt['vout']:
    out += i['scriptPubKey']['hex']
    print len(out)
print len(rt['vin'])

size = len(vin + out)/2+41*len(rt['vin'])+9*len(rt['vout'])+8+2
print 'size:　%s:'%size
print '%.8f '%float(size/1024.0*0.00001)

fee = 0.00001
is_ok = rpc_connection.settxfee(fee)
print is_ok
amount = 1
address = 'mt75PpVcfjceTcCn1C8qgJr4ext2F31udd'
txid = rpc_connection.sendtoaddress(address,amount,'coffee','foryou',True)




