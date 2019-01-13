#!/usr/bin/python3

## TODO : ALWAYS ENCRYPT BEFORE IF NO ENCRYPTED FILE

import sys
from keeper         import Keeper
from config.default import CONFIG

def main():
    keeper 	= Keeper(CONFIG)
    options = sys.argv[1:]
    comm    = keeper.comm(options) if len(options) <= 2 else False

    if comm and callable(comm): 
        print(comm())
    else:
	    print(comm)


if __name__ == '__main__':
    main()