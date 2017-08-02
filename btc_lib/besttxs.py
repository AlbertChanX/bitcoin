from walletinfo import get_rpc
import math
rpc_connection = get_rpc()

txs = rpc_connection.getblocktemplate()
tx_tmp = txs['transactions']
txs_length = len(tx_tmp)
print(tx_tmp)
for i, tx in enumerate(tx_tmp):
    # tx['index'] = i+1
    print(i+1, tx['fee'], tx['txid'], tx['fee']/len(tx['data'])*2.0, tx['depends'])

# for i, tx in enumerate(sorted(tx_tmp, key=lambda k: tx['fee']/len(tx['data'])*2.000, reverse=True)):
#     print(i+1, tx['fee'], tx['txid'])


print(txs_length)



def hacks_antminer_s9_work(work):
    """
    Ant-miner S9 can not work when merkle_branch length is 5, 7, 9.
    We must process work transactions count out range of [16-31], [64-127],
    [256-511]
    """

    def calc_fee(wk):
        return sum([tx['fee'] for tx in wk['transactions']])  # all fees

    txs_length = len(work['transactions'])
    if txs_length == 0:
        return work

    merkle_branch_lenght = int(math.floor(math.log(txs_length, 2)) + 1)
    merkle_branch_lenght = 5

    if merkle_branch_lenght in [5, 7, 9]:
        before_fee = calc_fee(work)
        depends = dict()  # depends tx
        valid = False

        for tx in work['transactions']:
            for j in tx['depends']:
                # print(valid)
                depends[j] = work['transactions'][j-1]   #

        print('Merkle branch length is %s, will process work data.' %
                  merkle_branch_lenght)
        work['transactions'] = sorted(work['transactions'],
                                      key=lambda k: k['fee']/len(k['data']), reverse=True)

        index = 2 ** (merkle_branch_lenght - 1) - 1

        work['transactions'] = work[
                    'transactions'][:index]
        pre_depends = {}
        for t in work['transactions']:
            for depend in t['depends']:
                print('depend is ', depend)
                pre_depends[depend] = depends[depend]
        print('index is', index)


        for tx_item in pre_depends.values():

            if tx_item not in work['transactions']:
                for _ in xrange(index):
                    if work['transactions'][index-1] in pre_depends.values():
                        index -= 1

                        if index == -1:
                            valid = False
                    else:
                        print('change index %s %s' % (index, tx_item['txid']))
                        work['transactions'][index] = tx_item
                        break

        for i, j in enumerate(work['transactions']):
            print(i+1, j)
        before_subsidy = work['coinbasevalue']
        work['coinbasevalue'] -= (before_fee - calc_fee(work))
        print('Work subsidy change: %s->%s' % (before_subsidy,
                                                   work['coinbasevalue']))

        return work

    return work


hacks_antminer_s9_work(txs)
