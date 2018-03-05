#!/usr/bin/env python

import sys, os, string, random, re
from assets.db_globals import Globals
from data.scrt import scrt
print(scrt)
options = [ sys.argv[x] for x in range(len(sys.argv)) if len(sys.argv) > 1 and x != 0 ]

db 	 	= Globals(scrt)
decrypt = db.read().decrypt().split('&&%%')

data_read = decrypt[1:len(decrypt)-1]
data_filter = None

if options :
	data_filter = db.switch(options[0], '('+options[1]+')', data_read)
else :
	data_filter = db.switch('', '(.+)', data_read)

table = data_filter()
print(table)
