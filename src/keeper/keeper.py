#!/usr/bin/env python

import os, re, base64

from table 					import Table
from Crypto.Cipher  import AES
from Crypto 				import Random

class Keeper:
	def __init__(self, _conf) :
		self.__key 		= _conf['key'].encode('utf8')[:32]
		self.__cipher 	= eval(_conf['aes'].format(self.__key))
		self.__d_path   = eval(_conf['d_path'])
		self.__e_path   = eval(_conf['e_path'])
		# TODO : REMOVE THIS, ONLY SUPPOSED TO BE CALLED IF NO e_path ON APP
		self.__encrypt()

	def __padding(self, _str):
		########	BYTE PADDING	########
		######## https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256#12525165
		######## http://www.codekoala.com/posts/aes-encryption-python-using-pycrypto/
		
		BLOCK_SIZE = 16
		PADDING = ' '

		return _str + (BLOCK_SIZE - len(_str) % BLOCK_SIZE) * PADDING
		
		#while len(_str) % 16 != 0:
		#	_str += '\0'

		#return _str
	
	def __encrypt(self) :
		file_exists = os.path.isfile(self.__d_path)

		if file_exists:
			try:
				read = open(self.__d_path, 'r').read()
				pad = self.__padding(read)
				encrypt = self.__cipher.encrypt(pad)
				encode = base64.b64encode(encrypt)

				file = open(self.__e_path, "wb+")
				file.write(encode)
			except Exception as error:
				print('ENCRYPT EXCEPTION :: {}'.format(str(error)))
				return error

		return True

	def __decrypt(self):
		###### DEMOROU PRA CARALHO PRA RESOLVER ISSO
		###### O DECRYPT VOLTA COM UMA STRING EM BYTES
		###### O DECODE('UTF8') E PRA PODER FAZER O RSTRIP
		###### https://www.dreamincode.net/forums/topic/383989-using-b64decode-in-python-3x/

		try:
			read = open(self.__e_path).read()
			decode = base64.b64decode(read)
			decrypt = self.__cipher.decrypt(decode).decode('utf8')
		except Exception as error:
			print('DECRYPT EXCEPTION :: {}'.format(str(error)))
			return error

		return decrypt.rstrip(' ')
		
	def comm(self, _command):
		array = self.__decrypt().split('&&%%')
		array = array[1:len(array)-1]
		
		table = Table(array)

		if len(_command) == 0:
			_command.append('')

		def company():
			index = 0
			company_array = []
			regex = '('+_command[1]+')' if _command[1] else '(.+)'

			while index < len(array)-1 :
				comp_line = array[index]
				regex_match = re.match(regex, comp_line)

				if regex_match :
					acc_line = array[index+1]
					pwd_line = array[index+2]

					company_array.append(comp_line)
					company_array.append(acc_line)
					company_array.append(pwd_line)

				index += 3

			table = Table(company_array)
			company_table = table.create()
			return company_table
			

		def account():
			index = 0
			account_array = []
			regex = '('+_command[1]+')' if _command[1] else '(.+)'

			while index < len(array)-1 :
				acc_line 		= array[index]
				regex_match = re.match(regex, acc_line)

				if regex_match :
					comp_line = array[index-1]
					pwd_line = array[index+1]

					account_array.append(comp_line)
					account_array.append(acc_line)
					account_array.append(pwd_line)

				index += 1

			table = Table(account_array)
			account_table = table.create()
			return account_table

		def default():
			table_default = table.create()
			return table_default

		try: 
			commands = {
				'-c' : company,
				'-a' : account,
				''	 : default
			}[_command[0]]
		except Exception:
			message = 'Command not found or missing!'
			return message

		return commands

