from decimal import Decimal
l = [['a',value] for value in range(10)]

print l[0:2]

a = dict()
key = 'sfs'
a.setdefault(key,1)

print a

print 'on %s %s'%('hhh','ok')

print 'sdv  %s'%'cc'

###scriptPubKey
hex = '76a9141dc28cc5a04a4458a88b9502cb835e2c770865a788ac'
print len(hex)

in_hex = '7304402204355b5baac30eb3729c579855d1bece9613cf4edccef1520e7beca04f7e637170220068f8edd276dbd74a1ade0f25855578e274faa5d3838c6449ebc6be18b5c458301210269eacba4a571fd8802e3725e7bc1d1c590464a3348189fbf267bf2216898ed3b'


print len(in_hex)


d = {1:'s',2:'se'}
print len(d)

import urlparse

s = urlparse.urlparse('http://cyc:123@127.0.0.1:18332')
print s.password,s.username



